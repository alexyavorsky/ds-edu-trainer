/** Вопрос с выбором <Quiz>: отметка верного варианта и объяснение. Общий для уроков Python и английского. */
export function initQuiz(root: HTMLElement): void {
  const feedback = root.querySelector<HTMLElement>('[data-feedback]')!;
  const explain = root.querySelector<HTMLElement>('[data-explain]');
  const options = [...root.querySelectorAll<HTMLButtonElement>('[data-option]')];
  let wrong = 0;
  for (const option of options) {
    option.addEventListener('click', () => {
      const correct = option.hasAttribute('data-correct');
      option.classList.add(correct ? 'is-correct' : 'is-wrong');
      if (correct) {
        options.forEach((o) => (o.disabled = true));
        feedback.textContent = 'Верно!';
        feedback.className = 'quiz-feedback is-pass';
        if (explain) explain.hidden = false;
        return;
      }
      option.disabled = true;
      wrong++;
      feedback.textContent = wrong === 1 ? 'Не совсем — попробуйте ещё раз.' : 'Снова мимо. Подсказка — в тексте выше; или выберите другой вариант.';
      feedback.className = 'quiz-feedback is-fail';
    });
  }
}
