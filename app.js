// ========== Poogo - اپلیکیشن اصلی ==========

// ---------- داده پرامت‌ها ----------
const promptsData = [
  { id: 1, category: 'writing', title: 'نویسنده مقاله SEO', text: 'تو یک نویسنده حرفه‌ای هستی. یک مقاله SEO با کلمات کلیدی [موضوع] بنویس، حداقل ۸۰۰ کلمه، با مقدمه جذاب و پاراگراف‌های ساختاریافته.', tag: 'نویسندگی' },
  { id: 2, category: 'writing', title: 'خلاصه‌ساز متن', text: 'متن زیر را خلاصه کن و نکات کلیدی را به صورت بولت استخراج کن:\n\n[متن شما]', tag: 'نویسندگی' },
  { id: 3, category: 'code', title: 'توضیح کد', text: 'این کد را خط به خط توضیح بده و بگو هر بخش چه کاری انجام می‌دهد:\n\n```\n[کد شما]\n```', tag: 'برنامه‌نویسی' },
  { id: 4, category: 'code', title: 'رفع باگ', text: 'باگ این کد را پیدا کن و نسخه اصلاح‌شده را بنویس. زبان: [زبان].\n\n[کد شما]', tag: 'برنامه‌نویسی' },
  { id: 5, category: 'code', title: 'تبدیل به تابع', text: 'این منطق را به یک تابع تمیز و قابل استفاده تبدیل کن. زبان: [زبان].\n\n[منطق یا کد فعلی]', tag: 'برنامه‌نویسی' },
  { id: 6, category: 'creative', title: 'ایده استارتاپ', text: '۵ ایده استارتاپ نوآورانه در حوزه [حوزه] پیشنهاد بده. برای هر کدام مشکل، راه‌حل و مدل درآمد را بنویس.', tag: 'خلاقانه' },
  { id: 7, category: 'creative', title: 'داستان کوتاه', text: 'یک داستان کوتاه (۳۰۰ کلمه) بنویس با موضوع [موضوع]. لحن: [لحن].', tag: 'خلاقانه' },
  { id: 8, category: 'business', title: 'ایمیل فروش', text: 'یک ایمیل فروش حرفه‌ای برای [محصول/خدمت] بنویس. مخاطب: [مخاطب]. CTA واضح داشته باشد.', tag: 'کسب‌وکار' },
  { id: 9, category: 'business', title: 'پلن بازاریابی', text: 'یک پلن بازاریابی ۳۰ روزه برای [محصول] در شبکه‌های اجتماعی بنویس. شامل پست، هشتگ و زمان‌بندی.', tag: 'کسب‌وکار' },
  { id: 10, category: 'education', title: 'توضیح ساده مفهوم', text: 'مفهوم [مفهوم] را طوری توضیح بده که یک نوجوان ۱۴ ساله بفهمد. با مثال روزمره.', tag: 'آموزش' },
  { id: 11, category: 'education', title: 'سوال امتحانی', text: '۱۰ سوال چندگزینه‌ای و ۵ سوال تشریحی برای مبحث [مبحث] سطح [پایه/دانشگاه] بساز.', tag: 'آموزش' },
  { id: 12, category: 'translate', title: 'ترجمه تخصصی', text: 'متن زیر را به [زبان مقصد] ترجمه کن. لحن رسمی/غیررسمی. اصطلاحات تخصصی را درست منتقل کن.\n\n[متن]', tag: 'ترجمه' },
  { id: 13, category: 'translate', title: 'بازنویسی و ساده‌سازی', text: 'متن زیر را بازنویسی کن تا ساده‌تر و خواناتر شود، بدون از دست دادن معنا.\n\n[متن]', tag: 'ترجمه' },
];

// ---------- رندر پرامت‌ها ----------
function renderPrompts(category = 'all') {
  const grid = document.getElementById('promptsGrid');
  const filtered = category === 'all' ? promptsData : promptsData.filter(p => p.category === category);
  grid.innerHTML = filtered.map(p => `
    <div class="prompt-card" data-id="${p.id}">
      <h4>${p.title}</h4>
      <p>${p.text.slice(0, 100)}...</p>
      <span class="tag">${p.tag}</span>
    </div>
  `).join('');
  grid.querySelectorAll('.prompt-card').forEach(card => {
    card.addEventListener('click', () => {
      const p = promptsData.find(x => x.id == card.dataset.id);
      document.getElementById('modalPromptTitle').textContent = p.title;
      document.getElementById('modalPromptText').textContent = p.text;
      document.getElementById('promptModal').classList.add('active');
      document.getElementById('promptModal').dataset.currentText = p.text;
    });
  });
}

document.querySelectorAll('.cat-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.cat-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    renderPrompts(btn.dataset.cat);
  });
});

const promptModal = document.getElementById('promptModal');
promptModal.querySelector('.modal-close').addEventListener('click', () => promptModal.classList.remove('active'));
promptModal.querySelector('.copy-prompt').addEventListener('click', () => {
  const text = promptModal.dataset.currentText || '';
  navigator.clipboard.writeText(text).then(() => alert('پرامت کپی شد.'));
});

// ---------- پیامرسانی ----------
const emojis = '😀 😃 😄 😁 😅 😂 🤣 🙂 🙃 😉 😊 😇 🥰 😍 🤩 😘 😗 ☺ 😚 😙 🥲 😋 😛 😜 🤪 😝 🤑 🤗 🤭 🤫 🤔 🤐 🤨 😐 😑 😶 😏 😒 🙄 😬 🤥 😌 😔 😪 🤤 😴 😷 🤒 🤕 🤢 🤮 🤧 🥵 🥶 🥴 😵 🤯 🤠 🥳 🥸 😎 🤓 🧐'.split(' ');
let conversations = [
  { id: 1, name: 'پشتیبانی Poogo', preview: 'سلام، چطور می‌تونم کمک کنم؟', unread: 0 },
  { id: 2, name: 'تیم فنی', preview: 'بروزرسانی Grafjy منتشر شد.', unread: 1 },
  { id: 3, name: 'گروه آموزش', preview: 'جلسه فردا ساعت ۱۸', unread: 0 },
];
let messagesByConv = {
  1: [
    { text: 'سلام، چطور می‌تونم کمک کنم؟', time: '۱۰:۳۰', sent: false },
  ],
  2: [
    { text: 'بروزرسانی Grafjy منتشر شد.', time: '۰۹:۱۵', sent: false },
  ],
  3: [
    { text: 'جلسه فردا ساعت ۱۸', time: 'دیروز', sent: false },
  ],
};
let currentConvId = null;

function renderConversations() {
  const list = document.getElementById('conversationsList');
  list.innerHTML = conversations.map(c => `
    <li class="conversation-item ${currentConvId === c.id ? 'active' : ''}" data-id="${c.id}">
      <div class="avatar">${c.name.charAt(0)}</div>
      <div class="conv-info">
        <div class="conv-name">${c.name}</div>
        <div class="conv-preview">${c.preview}</div>
      </div>
    </li>
  `).join('');
  list.querySelectorAll('.conversation-item').forEach(el => {
    el.addEventListener('click', () => {
      currentConvId = parseInt(el.dataset.id, 10);
      document.getElementById('currentChatName').textContent = conversations.find(c => c.id === currentConvId).name;
      document.getElementById('emptyChat').classList.add('hidden');
      const msgs = document.getElementById('messages');
      msgs.innerHTML = (messagesByConv[currentConvId] || []).map(m => `
        <div class="msg ${m.sent ? 'sent' : 'received'}">
          ${m.text}
          <time>${m.time}</time>
        </div>
      `).join('');
      renderConversations();
    });
  });
}

function sendMessage() {
  const input = document.getElementById('messageInput');
  const text = input.value.trim();
  if (!text || !currentConvId) return;
  if (!messagesByConv[currentConvId]) messagesByConv[currentConvId] = [];
  const now = new Date();
  const timeStr = now.getHours().toString().padStart(2, '0') + ':' + now.getMinutes().toString().padStart(2, '0');
  messagesByConv[currentConvId].push({ text, time: timeStr, sent: true });
  const conv = conversations.find(c => c.id === currentConvId);
  conv.preview = text;
  input.value = '';
  const msgs = document.getElementById('messages');
  msgs.innerHTML = messagesByConv[currentConvId].map(m => `
    <div class="msg ${m.sent ? 'sent' : 'received'}">
      ${m.text}
      <time>${m.time}</time>
    </div>
  `).join('');
  renderConversations();
}

document.getElementById('sendMessage').addEventListener('click', sendMessage);
document.getElementById('messageInput').addEventListener('keydown', e => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

document.querySelector('.new-chat').addEventListener('click', () => {
  const name = prompt('نام مکالمه جدید:') || 'مکالمه جدید';
  const id = Math.max(...conversations.map(c => c.id), 0) + 1;
  conversations.unshift({ id, name, preview: 'شروع مکالمه', unread: 0 });
  messagesByConv[id] = [];
  currentConvId = id;
  document.getElementById('currentChatName').textContent = name;
  document.getElementById('emptyChat').classList.add('hidden');
  document.getElementById('messages').innerHTML = '';
  renderConversations();
});

// ایموجی
const emojiPicker = document.getElementById('emojiPicker');
emojiPicker.innerHTML = emojis.map(e => `<span>${e}</span>`).join('');
emojis.forEach((e, i) => {
  emojiPicker.children[i].addEventListener('click', () => {
    document.getElementById('messageInput').value += e;
  });
});
document.querySelector('.emoji-trigger').addEventListener('click', () => emojiPicker.classList.toggle('active'));
document.getElementById('attachBtn').addEventListener('click', () => document.getElementById('attachFile').click());

renderConversations();

// ---------- Grafjy اجرا (مفسر ساده) ----------
function runGrafjy() {
  const code = document.getElementById('grafjyCode').value;
  const out = document.getElementById('grafjyOutput');
  const lines = code.split('\n').map(l => l.trim()).filter(Boolean);
  const output = [];
  const replies = [];

  function time() {
    return new Date().toLocaleTimeString('fa-IR', { hour: '2-digit', minute: '2-digit' });
  }

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    if (line.startsWith('#')) continue;
    const onMessage = line.match(/on message\s+"([^"]+)":/);
    const onKeyword = line.match(/on keyword\s+"([^"]+)":/);
    if (onMessage) {
      output.push(`[رویداد] message "${onMessage[1]}" ثبت شد.`);
      continue;
    }
    if (onKeyword) {
      output.push(`[رویداد] keyword "${onKeyword[1]}" ثبت شد.`);
      continue;
    }
    const replyMatch = line.match(/reply\s+"([^"]+)"|reply\s+(.+)/);
    if (replyMatch) {
      let msg = replyMatch[1] || replyMatch[2];
      if (msg.includes('+')) {
        try {
          msg = msg.replace(/time\(\)/g, '"' + time() + '"');
          msg = msg.replace(/\s*\+\s*/g, ' ');
          msg = msg.replace(/"/g, '').trim();
        } catch (_) {}
      }
      replies.push(msg);
      output.push(`[پاسخ] ${msg}`);
    }
  }

  if (output.length === 0) output.push('خروجی: هیچ دستوری اجرا نشد. سینتکس را بررسی کنید.');
  out.textContent = output.join('\n');
}

document.getElementById('runGrafjy').addEventListener('click', runGrafjy);
document.getElementById('clearGrafjy').addEventListener('click', () => {
  document.getElementById('grafjyCode').value = '';
  document.getElementById('grafjyOutput').textContent = '';
});
document.getElementById('saveGrafjy').addEventListener('click', () => {
  const code = document.getElementById('grafjyCode').value;
  localStorage.setItem('poogo_grafjy_saved', code);
  alert('کد ذخیره شد.');
});
if (localStorage.getItem('poogo_grafjy_saved')) {
  document.getElementById('grafjyCode').value = localStorage.getItem('poogo_grafjy_saved');
}

// ---------- ویرایشگر عکس ----------
const canvas = document.getElementById('mainCanvas');
const ctx = canvas.getContext('2d');
const CANVAS_W = 800, CANVAS_H = 500;
canvas.width = CANVAS_W;
canvas.height = CANVAS_H;
ctx.fillStyle = '#2a2a35';
ctx.fillRect(0, 0, CANVAS_W, CANVAS_H);
let canvasBase = null; // پس‌زمینه بدون متن (برای بازکشیدن موقع تغییر متن)
function saveCanvasBase() {
  canvasBase = document.createElement('canvas');
  canvasBase.width = canvas.width;
  canvasBase.height = canvas.height;
  canvasBase.getContext('2d').drawImage(canvas, 0, 0);
}
saveCanvasBase();

const fonts = [
  'Vazirmatn', 'Tahoma', 'Arial', 'Georgia', 'Courier New', 'Impact',
  'B Nazanin', 'B Titr', 'B Mitra', 'B Yekan', 'Samim', 'Shabnam',
  'Segoe UI', 'JetBrains Mono', 'Consolas', 'Times New Roman'
];
const fontSelect = document.getElementById('fontSelect');
fonts.forEach(f => {
  const opt = document.createElement('option');
  opt.value = f;
  opt.textContent = f;
  fontSelect.appendChild(opt);
});

const templateColors = [
  '#1a1a2e', '#16213e', '#0f3460', '#e94560', '#00d4aa', '#7c5cff',
  '#2d132c', '#ee4540', '#c72c41', '#801336', '#fbe555', '#2ec4b6'
];
const templatesGrid = document.getElementById('templatesGrid');
for (let i = 0; i < 12; i++) {
  const c = templateColors[i];
  const thumb = document.createElement('div');
  thumb.className = 'template-thumb';
  thumb.style.background = c;
  thumb.dataset.color = c;
  thumb.addEventListener('click', () => {
    ctx.fillStyle = c;
    ctx.fillRect(0, 0, CANVAS_W, CANVAS_H);
    saveCanvasBase();
    document.querySelectorAll('.template-thumb').forEach(t => t.classList.remove('active'));
    thumb.classList.add('active');
  });
  templatesGrid.appendChild(thumb);
}

const filterNames = ['عادی', 'خاکستری', 'سپیا', 'معکوس', 'تاریک', 'روشن'];
const filtersGrid = document.getElementById('filtersGrid');
filterNames.forEach((name, i) => {
  const thumb = document.createElement('canvas');
  thumb.className = 'filter-thumb';
  thumb.width = 60;
  thumb.height = 60;
  const tctx = thumb.getContext('2d');
  tctx.fillStyle = ['#888', '#555', '#6b5344', '#333', '#222', '#ddd'][i];
  tctx.fillRect(0, 0, 60, 60);
  tctx.fillStyle = '#fff';
  tctx.font = '10px Vazirmatn';
  tctx.fillText(name, 4, 32);
  thumb.addEventListener('click', () => applyFilter(i));
  filtersGrid.appendChild(thumb);
});

function applyFilter(type) {
  const imgData = ctx.getImageData(0, 0, canvas.width, canvas.height);
  const d = imgData.data;
  for (let i = 0; i < d.length; i += 4) {
    const r = d[i], g = d[i+1], b = d[i+2];
    if (type === 1) {
      const gray = 0.299 * r + 0.587 * g + 0.114 * b;
      d[i] = d[i+1] = d[i+2] = gray;
    } else if (type === 2) {
      d[i] = r * 0.393 + g * 0.769 + b * 0.189;
      d[i+1] = r * 0.349 + g * 0.686 + b * 0.168;
      d[i+2] = r * 0.272 + g * 0.534 + b * 0.131;
    } else if (type === 3) {
      d[i] = 255 - r;
      d[i+1] = 255 - g;
      d[i+2] = 255 - b;
    } else if (type === 4) {
      d[i] *= 0.5; d[i+1] *= 0.5; d[i+2] *= 0.5;
    } else if (type === 5) {
      d[i] = Math.min(255, r * 1.2);
      d[i+1] = Math.min(255, g * 1.2);
      d[i+2] = Math.min(255, b * 1.2);
    }
  }
  ctx.putImageData(imgData, 0, 0);
  saveCanvasBase();
}

document.getElementById('uploadImage').addEventListener('change', e => {
  const file = e.target.files[0];
  if (!file) return;
  const img = new Image();
  img.onload = () => {
    canvas.width = img.width;
    canvas.height = img.height;
    ctx.drawImage(img, 0, 0);
    saveCanvasBase();
  };
  img.src = URL.createObjectURL(file);
});

document.getElementById('newCanvas').addEventListener('click', () => {
  canvas.width = CANVAS_W;
  canvas.height = CANVAS_H;
  ctx.fillStyle = '#2a2a35';
  ctx.fillRect(0, 0, CANVAS_W, CANVAS_H);
  saveCanvasBase();
});

document.getElementById('textOverlay').addEventListener('input', drawTextOnCanvas);
document.getElementById('fontSelect').addEventListener('change', drawTextOnCanvas);
document.getElementById('textColor').addEventListener('input', drawTextOnCanvas);
document.getElementById('fontSize').addEventListener('input', e => {
  document.getElementById('fontSizeLabel').textContent = e.target.value + 'px';
  drawTextOnCanvas();
});

function drawTextOnCanvas() {
  const text = document.getElementById('textOverlay').value;
  if (!canvasBase) return;
  ctx.drawImage(canvasBase, 0, 0);
  if (!text) return;
  const font = document.getElementById('fontSelect').value;
  const color = document.getElementById('textColor').value;
  const size = parseInt(document.getElementById('fontSize').value, 10);
  ctx.font = `${size}px ${font}`;
  ctx.fillStyle = color;
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillText(text, canvas.width / 2, canvas.height / 2);
}

document.getElementById('downloadImage').addEventListener('click', () => {
  const a = document.createElement('a');
  a.download = 'poogo-image.png';
  a.href = canvas.toDataURL('image/png');
  a.click();
});

document.getElementById('undoCanvas').addEventListener('click', () => {
  ctx.fillStyle = '#2a2a35';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
});

// ---------- آموزش Grafjy ----------
const lessons = {
  intro: {
    title: 'مقدمه Grafjy',
    content: `
      <h3>Grafjy چیست؟</h3>
      <p>Grafjy زبان برنامه‌نویسی اختصاصی پلتفرم Poogo است که برای ساخت ربات‌های پیامرسان طراحی شده است. با دستورات ساده می‌توانید به پیام‌های کاربران واکنش نشان دهید و پاسخ خودکار بفرستید.</p>
      <h3>چرا Grafjy؟</h3>
      <p>نیازی به نصب یا تنظیم سرور نیست. کد را می‌نویسید، اجرا می‌کنید و ربات شما آماده است. سینتکس شبیه زبان‌های خوانا و نزدیک به انگلیسی است.</p>
      <pre># این یک comment است
on message "سلام":
    reply "سلام! چطور می‌تونم کمک کنم؟"</pre>
    `
  },
  syntax: {
    title: 'سینتکس پایه',
    content: `
      <h3>ساختار دستورات</h3>
      <p>هر دستور در یک خط نوشته می‌شود. خطوطی که با <code>#</code> شروع می‌شوند توضیح (comment) هستند.</p>
      <pre># توضیح
on message "کلید":
    reply "پاسخ"</pre>
      <h3>بلوک‌ها</h3>
      <p>دستورات مربوط به یک رویداد با تورفتگی (indent) زیر همان رویداد قرار می‌گیرند.</p>
    `
  },
  events: {
    title: 'رویدادها',
    content: `
      <h3>on message "متن"</h3>
      <p>وقتی کاربر دقیقاً این متن را فرستاد، دستورات زیر اجرا می‌شوند.</p>
      <pre>on message "زمان":
    reply "الان " + time()</pre>
      <h3>on keyword "کلمه"</h3>
      <p>اگر پیام کاربر شامل این کلمه باشد (هر جای پیام)، دستورات اجرا می‌شوند.</p>
      <pre>on keyword "کمک":
    reply "دستورات: زمان، کمک، سلام"</pre>
    `
  },
  variables: {
    title: 'متغیرها و توابع',
    content: `
      <h3>توابع داخلی</h3>
      <p><code>time()</code> — زمان فعلی را برمی‌گرداند.</p>
      <p>می‌توانید با <code>+</code> متن‌ها را به هم بچسبانید.</p>
      <pre>reply "امروز " + date() + " است."</pre>
      <h3>ساختار شرطی</h3>
      <p>در نسخه‌های بعدی: شرط if و حلقه‌ها اضافه می‌شوند.</p>
    `
  },
  advanced: {
    title: 'پیشرفته',
    content: `
      <h3>چند رویداد برای یک پاسخ</h3>
      <p>می‌توانید برای چند عبارت مختلف یک پاسخ مشترک بگذارید:</p>
      <pre>on message "سلام":
    reply "سلام!"
on message "سلام علیک":
    reply "سلام!"
on keyword "خداحافظ":
    reply "موفق باشید."</pre>
      <h3>بهترین روش‌ها</h3>
      <p>پرامت‌های واضح بنویسید. پاسخ‌ها را کوتاه و مفید نگه دارید. از comment برای توضیح منطق استفاده کنید.</p>
    `
  }
};

function renderLesson(lessonId) {
  const lesson = lessons[lessonId] || lessons.intro;
  document.getElementById('learnContent').innerHTML = `<h2>${lesson.title}</h2>${lesson.content}`;
}

document.querySelectorAll('.learn-nav-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.learn-nav-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    renderLesson(btn.dataset.lesson);
  });
});
renderLesson('intro');

// ---------- زبان‌های برنامه‌نویسی و دوره‌ها ----------
const domainLabels = { web: 'وب', mobile: 'موبایل', ai: 'هوش مصنوعی', game: 'بازی', backend: 'سرور', data: 'داده و تحلیل' };
const languagesData = [
  { name: 'JavaScript', domain: 'web', desc: 'زبان اصلی وب؛ فرانت و بکند با Node.js. یادگیری آسان و بازار کار عالی.' },
  { name: 'Python', domain: 'ai', desc: 'پیشرو در هوش مصنوعی، داده و اتوماسیون. خوانا و همه‌کاره.' },
  { name: 'TypeScript', domain: 'web', desc: 'JavaScript با تایپ امن؛ مناسب پروژه‌های بزرگ و تیم‌ها.' },
  { name: 'Swift', domain: 'mobile', desc: 'زبان رسمی اپل برای iOS و macOS. مدرن و سریع.' },
  { name: 'Kotlin', domain: 'mobile', desc: 'زبان پیشنهادی برای اندروید؛ هم‌زیستی با Java.' },
  { name: 'C#', domain: 'game', desc: 'با Unity برای ساخت بازی؛ همچنین دسکتاپ و وب.' },
  { name: 'C++', domain: 'game', desc: 'برای بازی‌های سنگین و موتورهای بازی؛ کارایی بالا.' },
  { name: 'Go', domain: 'backend', desc: 'ساده و سریع؛ ایده‌آل برای سرویس‌ها و میکروسرویس.' },
  { name: 'Rust', domain: 'backend', desc: 'امنیت حافظه و سرعت؛ برای سیستم‌های حیاتی.' },
  { name: 'R', domain: 'data', desc: 'تحلیل آماری و نمودار؛ استاندارد در علم داده.' },
  { name: 'SQL', domain: 'data', desc: 'زبان استاندارد پایگاه داده؛ ضروری برای هر توسعه‌دهنده.' },
  { name: 'PHP', domain: 'web', desc: 'سرور وب؛ وردپرس و بسیاری از CMSها.' },
];

const coursesData = [
  { title: 'JavaScript از صفر', lang: 'JavaScript', level: 'مقدماتی', duration: '۴۰ ساعت', desc: 'از متغیر و تابع تا DOM و Async. پروژه‌های عملی.' },
  { title: 'Python برای همه', lang: 'Python', level: 'مقدماتی', duration: '۳۰ ساعت', desc: 'سینتکس، ساختار داده، فایل و مقدمه وب و داده.' },
  { title: 'توسعه وب با React', lang: 'JavaScript/React', level: 'متوسط', duration: '۵۰ ساعت', desc: 'کامپوننت، state، React Hooks و پروژه واقعی.' },
  { title: 'اندروید با Kotlin', lang: 'Kotlin', level: 'متوسط', duration: '۶۰ ساعت', desc: 'Activity، Fragment، API و انتشار اپ.' },
  { title: 'یادگیری ماشین با Python', lang: 'Python', level: 'پیشرفته', duration: '۸۰ ساعت', desc: 'Scikit-learn، TensorFlow و پروژه‌های ML.' },
  { title: 'بازی با Unity و C#', lang: 'C#', level: 'متوسط', duration: '۷۰ ساعت', desc: 'فیزیک، انیمیشن، UI و انتشار بازی.' },
  { title: 'Go برای بکند', lang: 'Go', level: 'متوسط', duration: '۲۵ ساعت', desc: 'سرویس REST، دیتابیس و Docker.' },
  { title: 'تحلیل داده با R و SQL', lang: 'R / SQL', level: 'مقدماتی', duration: '۳۵ ساعت', desc: 'پرس‌وجو، تجسم و گزارش.' },
];

function renderLanguages(domain = 'all') {
  const grid = document.getElementById('languagesGrid');
  const filtered = domain === 'all' ? languagesData : languagesData.filter(l => l.domain === domain);
  grid.innerHTML = filtered.map(l => `
    <div class="lang-card">
      <h4>${l.name}</h4>
      <div class="domain">${domainLabels[l.domain] || l.domain}</div>
      <p>${l.desc}</p>
    </div>
  `).join('');
}

document.querySelectorAll('.lang-tab').forEach(tab => {
  tab.addEventListener('click', () => {
    document.querySelectorAll('.lang-tab').forEach(t => t.classList.remove('active'));
    tab.classList.add('active');
    renderLanguages(tab.dataset.domain);
  });
});

function renderCourses() {
  const grid = document.getElementById('coursesGrid');
  grid.innerHTML = coursesData.map(c => `
    <div class="course-card">
      <h4>${c.title}</h4>
      <div class="course-meta">${c.lang} · ${c.level} · ${c.duration}</div>
      <p>${c.desc}</p>
    </div>
  `).join('');
}

renderLanguages();
renderCourses();

// ---------- اسکرول ناوبری و منوی موبایل ----------
document.querySelectorAll('.nav-links a').forEach(a => {
  a.addEventListener('click', e => {
    const href = a.getAttribute('href');
    if (href.startsWith('#')) {
      e.preventDefault();
      document.querySelector(href)?.scrollIntoView({ behavior: 'smooth' });
    }
  });
});

document.querySelector('.nav-toggle').addEventListener('click', () => {
  document.querySelector('.nav-links').classList.toggle('open');
});

// رندر اولیه
renderPrompts();
