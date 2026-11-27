(() => {
  const root = document.documentElement;
  const themeButton = document.querySelector('[data-theme-toggle]');
  const getTheme = () => {
    try { return localStorage.getItem('mra-theme'); } catch { return null; }
  };
  const setTheme = theme => {
    root.dataset.theme = theme;
    if (themeButton) {
      themeButton.textContent = theme === 'dark' ? 'Mode terang' : 'Mode gelap';
      themeButton.setAttribute('aria-label', `Gunakan ${theme === 'dark' ? 'mode terang' : 'mode gelap'}`);
    }
  };
  setTheme(getTheme() || (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'));
  if (themeButton) {
    themeButton.hidden = false;
    themeButton.addEventListener('click', () => {
      const theme = root.dataset.theme === 'dark' ? 'light' : 'dark';
      setTheme(theme);
      try { localStorage.setItem('mra-theme', theme); } catch { /* Reading works when storage is unavailable. */ }
    });
  }
  document.querySelectorAll('[data-print]').forEach(button => {
    button.hidden = false;
    button.addEventListener('click', () => window.print());
  });

  const search = document.querySelector('#topic-search');
  if (search) {
    document.querySelector('.search-area').hidden = false;
    const chapters = [...document.querySelectorAll('[data-chapter]')];
    const count = document.querySelector('#search-count');
    const empty = document.querySelector('#no-results');
    const normalize = value => value.toLocaleLowerCase('id').normalize('NFKC');
    const texts = chapters.map(chapter => normalize(chapter.textContent));
    const filter = () => {
      const words = normalize(search.value.trim()).split(/\s+/).filter(Boolean);
      let found = 0;
      chapters.forEach((chapter, index) => {
        const show = words.every(word => texts[index].includes(word));
        chapter.hidden = !show;
        if (show) found++;
      });
      count.textContent = `${found} dari ${chapters.length} topik ditampilkan.`;
      empty.hidden = found !== 0;
    };
    search.addEventListener('input', filter);
    document.querySelector('[data-clear-search]').addEventListener('click', () => {
      search.value = '';
      filter();
      search.focus();
    });
    document.querySelectorAll('a[href^="#topik-"]').forEach(link => {
      link.addEventListener('click', () => {
        search.value = '';
        filter();
      });
    });
    filter();
  }

  const results = new Map();
  const quizzes = [...document.querySelectorAll('[data-quiz]')];
  quizzes.forEach(quiz => {
    const checkButton = quiz.querySelector('[data-check]');
    checkButton.hidden = false;
    checkButton.addEventListener('click', () => {
      const selected = quiz.querySelector('input:checked');
      const feedback = quiz.querySelector('[data-feedback]');
      feedback.hidden = false;
      if (!selected) {
        feedback.querySelector('[data-result]').textContent = 'Pilih satu jawaban terlebih dahulu.';
        feedback.querySelector('[data-explanation]').hidden = true;
        return;
      }
      const correct = selected.value === quiz.dataset.answer;
      results.set(quiz.id, correct);
      feedback.querySelector('[data-result]').textContent = correct ? 'Tepat.' : 'Belum tepat. Perhatikan pembahasannya.';
      feedback.querySelector('[data-explanation]').hidden = false;
      const status = document.querySelector('#quiz-status');
      if (status) status.textContent = `${results.size} dari ${quizzes.length} soal sudah diperiksa. ${[...results.values()].filter(Boolean).length} jawaban terakhir tepat. Ulangi topik yang masih sulit.`;
    });
  });
  const contents = document.querySelector('.contents');
  if (contents) {
    const wide = matchMedia('(min-width: 72rem)');
    const update = () => { contents.open = wide.matches; };
    update();
    wide.addEventListener('change', update);
    contents.querySelector('summary').addEventListener('click', event => {
      if (wide.matches) event.preventDefault();
    });
  }
  let previouslyClosed = [];
  addEventListener('beforeprint', () => {
    previouslyClosed = [...document.querySelectorAll('details:not([open])')];
    previouslyClosed.forEach(detail => { detail.open = true; });
  });
  addEventListener('afterprint', () => previouslyClosed.forEach(detail => { detail.open = false; }));
})();
