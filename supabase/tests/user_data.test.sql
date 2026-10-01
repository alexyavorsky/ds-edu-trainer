-- Политики user_data на настоящем Postgres Supabase: `supabase test db` (локальный стек, Docker).
-- Без Docker то же проверяет node scripts/test_supabase_sql.ts.
begin;
create extension if not exists pgtap with schema extensions;
select plan(9);

insert into auth.users (id, email) values
  ('00000000-0000-0000-0000-00000000000a', 'test-a@ds-edu-trainer.vercel.app'),
  ('00000000-0000-0000-0000-00000000000b', 'test-b@ds-edu-trainer.vercel.app');

set local role authenticated;
select set_config('request.jwt.claims', '{"sub": "00000000-0000-0000-0000-00000000000a", "role": "authenticated"}', true);
select lives_ok($$ select public.merge_user_data('{"solved": {"t1": {"v": true, "t": 100}}}') $$, 'A пишет через merge_user_data');
select lives_ok($$ select public.merge_user_data('{"solved": {"t1": {"v": false, "t": 50}}}') $$, 'A отправляет старую запись');
select is((select value -> 't1' ->> 'v' from public.user_data where key = 'solved'), 'true', 'старая запись не затирает новую');
select throws_ok($$ insert into public.user_data (user_id, key, value) values ('00000000-0000-0000-0000-00000000000a', 'solved', '{}') $$, '42501', null, 'прямой insert запрещён');

select set_config('request.jwt.claims', '{"sub": "00000000-0000-0000-0000-00000000000b", "role": "authenticated"}', true);
select is((select count(*) from public.user_data), 0::bigint, 'B не видит строк A');
delete from public.user_data;
select set_config('request.jwt.claims', '{"sub": "00000000-0000-0000-0000-00000000000a", "role": "authenticated"}', true);
select is((select count(*) from public.user_data), 1::bigint, 'B не удалил строки A');

set local role anon;
select set_config('request.jwt.claims', '', true);
select throws_ok($$ select * from public.user_data $$, '42501', null, 'аноним не читает таблицу');
select throws_ok($$ select public.merge_user_data('{"solved": {"x": {"v": true, "t": 1}}}') $$, '42501', null, 'аноним не пишет');

set local role authenticated;
select set_config('request.jwt.claims', '{"sub": "00000000-0000-0000-0000-00000000000a", "role": "authenticated"}', true);
select public.delete_own_account();
reset role;
select is((select count(*) from public.user_data where user_id = '00000000-0000-0000-0000-00000000000a'), 0::bigint, 'удаление аккаунта удаляет строки');

select * from finish();
rollback;
