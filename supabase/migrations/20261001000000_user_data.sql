-- Сохранение прогресса пользователя (README, раздел «Аккаунты и Supabase»).
--
-- Одна таблица: строка = «ключ синхронизации» пользователя, value — словарь записей
-- {id записи: {..., "t": время изменения в мс}}. Ключи:
--   solved          «Решено» у задач            {задача: {v, t}}
--   course.ex       решённые упражнения          {урок/упражнение: {hash, t}}
--   course.done     отметка «Урок пройден»       {урок: {v, t}}
--   course.last     последний открытый урок      {курс: {lesson, t}}
--   code:<id>       код задачи или упражнения    {id: {code, starter, t} | {d: true, t}}
--
-- Пишет только функция merge_user_data: она сливает записи по одной, побеждает запись с бо́льшим t.
-- Поэтому два устройства не затирают друг друга, а повторная отправка ничего не портит.
-- Читать и удалять свои строки можно напрямую (RLS), писать в таблицу напрямую нельзя.

create table public.user_data (
  user_id    uuid not null references auth.users on delete cascade,
  key        text not null check (key ~ '^(solved|course\.(ex|done|last)|code:[a-z0-9][a-z0-9/_.-]{0,150})$'),
  value      jsonb not null check (jsonb_typeof(value) = 'object' and octet_length(value::text) <= 262144),
  updated_at timestamptz not null default now(),
  primary key (user_id, key)
);

create index user_data_updated on public.user_data (user_id, updated_at);

alter table public.user_data enable row level security;

create policy user_data_select_own on public.user_data
  for select to authenticated using (user_id = (select auth.uid()));
create policy user_data_delete_own on public.user_data
  for delete to authenticated using (user_id = (select auth.uid()));

revoke all on public.user_data from anon, authenticated;
grant select, delete on public.user_data to authenticated;

-- p_data = {ключ: {id записи: запись}}. Записи без числового t пропускаются.
create function public.merge_user_data(p_data jsonb)
returns void
language plpgsql
security definer
set search_path = ''
as $$
declare
  uid uuid := auth.uid();
  k text;
  entries jsonb;
  incoming jsonb;
begin
  if uid is null then
    raise exception 'not authenticated' using errcode = '42501';
  end if;
  if jsonb_typeof(p_data) is distinct from 'object' then
    raise exception 'p_data must be an object' using errcode = '22023';
  end if;

  for k, entries in select * from jsonb_each(p_data) loop
    if jsonb_typeof(entries) <> 'object' then
      continue;
    end if;
    select coalesce(jsonb_object_agg(e.key, e.value), '{}'::jsonb) into incoming
      from jsonb_each(entries) e
     where jsonb_typeof(e.value) = 'object' and jsonb_typeof(e.value -> 't') = 'number';
    if incoming = '{}'::jsonb then
      continue;
    end if;

    insert into public.user_data as d (user_id, key, value)
    values (uid, k, incoming)
    on conflict (user_id, key) do update set
      value = (
        select jsonb_object_agg(
                 coalesce(n.id, o.id),
                 case
                   when n.v is null then o.v
                   when o.v is null then n.v
                   when (n.v ->> 't')::numeric >= coalesce((o.v ->> 't')::numeric, -1) then n.v
                   else o.v
                 end)
          from (select key as id, value as v from jsonb_each(d.value)) o
          full join (select key as id, value as v from jsonb_each(excluded.value)) n on n.id = o.id
      ),
      updated_at = now();
  end loop;

  if (select count(*) from public.user_data where user_id = uid) > 3000 then
    raise exception 'too many rows' using errcode = '54000';
  end if;
end;
$$;

-- Удаление аккаунта самим пользователем: строки user_data удалятся каскадом.
create function public.delete_own_account()
returns void
language plpgsql
security definer
set search_path = ''
as $$
begin
  if auth.uid() is null then
    raise exception 'not authenticated' using errcode = '42501';
  end if;
  delete from auth.users where id = auth.uid();
end;
$$;

revoke all on function public.merge_user_data(jsonb) from public, anon;
revoke all on function public.delete_own_account() from public, anon;
grant execute on function public.merge_user_data(jsonb) to authenticated;
grant execute on function public.delete_own_account() to authenticated;
