let evt = new Event('click');
let preview = '';
let overlay = '';
let video = '';
let videoZone = '';
let streamerField = '';
let streamer = '';
let gameImg = '';
let profileImg = '';
let streamerInfo = '';
let channelInfo = '';
let previewStyle = '';
let loader = '';
let form = '';

let defaultStyle = {
  animation: 'drop',
  bottomBgColor: '#ffffff',
  bottomTextColor: '#1b1c1d',
  clipInfoBgColor: '#1b1c1d',
  clipInfoDivider: '#16b2ab',
  clipInfoTextColor: '#ffffff',
  clipZoneBorder: '#16b2ab',
  displayClip: 'on',
  displayClipInfo: 'on',
  imgBgColor: '#1b1c1d',
  showClipBorder: 'on',
  textFont: 'Sansation Regular' || 'Arial',
  topBgColor: '#16b2ab',
  topTextColor: '#ffffff',
  volume: 0.75
};

let animOptions = [
  { value: 'drop', name: 'Drop', selected: true },
  { value: 'fade', name: 'Fade' },
  { value: 'fade up', name: 'Fade up' },
  { value: 'fade down', name: 'Fade down' },
  { value: 'fade left', name: 'Fade left' },
  { value: 'fade right', name: 'Fade right' },
  { value: 'fly up', name: 'Fly up' },
  { value: 'fly down', name: 'Fly down' },
  { value: 'fly left', name: 'Fly left' },
  { value: 'fly right', name: 'Fly right' },
  { value: 'horizontal flip', name: 'Horizontal flip' },
  { value: 'scale', name: 'Scale' },
  { value: 'slide up', name: 'Slide up' },
  { value: 'slide down', name: 'Slide down' },
  { value: 'slide left', name: 'Slide left' },
  { value: 'slide right', name: 'Slide right' },
  { value: 'swing up', name: 'Swing up' },
  { value: 'swing down', name: 'Swing down' },
  { value: 'swing left', name: 'Swing left' },
  { value: 'swing right', name: 'Swing right' },
  { value: 'vertical flip', name: 'Vertical flip' },
  { value: 'zoom', name: 'Zoom' },
];

$(document).ready(() => {
  preview = document.getElementById('preview');
  overlay = document.getElementById('overlay');
  video = document.querySelector('video');
  videoZone = document.getElementById('clipZone');
  streamerField = document.getElementById('streamerTag');
  profileImg = document.getElementById('profileImg');
  profileZone - document.getElementById('profileZone');
  gameImg = document.getElementById('gameImg');
  gameZone = document.getElementById('gameZone');
  streamerInfo = document.getElementById('streamerInfo');
  channelInfo = document.getElementById('channelInfo');
  streamer = $(streamerField).val() || 'von_schappler';
  images = document.querySelectorAll('img');
  loader = document.getElementById('loader');
  form = document.getElementById('form');
  setStyles(defaultStyle);
  dropOptions('animSelector', animOptions);
  $('.ui.dropdown').dropdown();
  $(form).form();
  document.dispatchEvent(evt);
  video.muted = true;
});

const setStyles = async (styles = defaultStyle) => {
  streamer = $(streamerField).val() || 'von_schappler';
  let previewStyle = document.getElementById('previewStyle');
  let clipInfo;
  const info = await getStreamerInfo(streamer);
  console.log(styles.textFont.length);
  gameImg.src = info.lastGameSrc;
  profileImg.src = info.avatarSrc;
  previewStyle.textContent = `
        @font-face {
          font-family: 'preview-font';
          src: local("${styles.textFont || defaultStyle.textFont}");
        }`;
  streamerInfo.innerText = `Follow ${streamer}\n(last saw playing ${info.lastGameName})`;
  $(streamerInfo).css({
    color: styles.topTextColor,
    'background-color': styles.topBgColor,
    'font-family': 'preview-font',
  });
  console.log(previewStyle);
  channelInfo.innerText = `at https://twitch.tv/${streamer}`;
  $(channelInfo).css({
    color: styles.bottomTextColor,
    'background-color': styles.bottomBgColor,
    'font-family': 'preview-font',
  });
  $(overlay).css({
    color: styles.clipInfoTextColor,
    'background-color': styles.clipInfoBgColor,
    'font-family': 'preview-font',
    'border-color': styles.clipInfoDivider,
  });
  $(gameZone).css({ 'background-color': styles.imgBgColor });
  $(profileZone).css({ 'background-color': styles.imgBgColor });
  $(videoZone).css({
    border: `${
      styles.showClipBorder
        ? `solid 3px ${styles.clipZoneBorder || defaultStyle.clipZoneBorder}`
        : 'none'
    }`,
  });

  if (styles.displayClip) {
    clipInfo = await getClipInfo(streamer);
    console.log('Clip played');
    videoZone.classList.remove('hidden');
  } else {
    videoZone.classList.add('hidden');
  }
  if (styles.displayClipInfo) {
    console.log('Clip info displayed');
    overlay.classList.remove('hidden');
  } else {
    overlay.classList.add('hidden');
  }
  if (styles.displayClip && clipInfo && info) {
    document.dispatchEvent(evt);
    renderClip(clipInfo, styles);
  }
  if (JSON.stringify(styles) !== JSON.stringify(defaultStyle))
    animOverlay(clipInfo?.duration, styles);
};

const renderClip = (info) => {
  document.dispatchEvent(evt);
  video.src = info.url;
  overlay.innerText = `${info.title} - featuring ${info.gameName}`;
  video.controls = false;
  video.muted = false;
  video.volume = 0.75;
};

const animOverlay = (clipDuration = 10, styles) => {
  document.dispatchEvent(evt);
  video.play()
  video.muted = false;
  loader.classList.add('active');
  $(preview).transition({
    verbose: true,
    animation: `${styles.animation} in`,
    duration: '1500ms',
    onComplete: function () {
      $(preview).transition({
        animation: `${styles.animation} out`,
        duration: '1500ms',
        interval: (clipDuration - 1) * 1000,
        onComplete: function () {
          video.muted = true;
          video.src = '';
          loader.classList.remove('active');
        },
      });
    },
  });
};

const getClipInfo = async (streamer) => {
  const clipRes = await fetch(
    `https://twitchapi.teklynk.com/getuserclips.php?channel=${streamer}&limit=10&dateRange=365`
  );
  const { data: clipData } = await clipRes.json();
  if (clipData.length === 0) return null;
  const clipIndex = Math.floor(Math.random() * clipData.length);
  const { clip_url: url, duration, title, id, game_id } = clipData[clipIndex];
  console.log({ url, duration, title, id, game_id });
  const gameRes = await fetch(
    `https://twitchapi.teklynk.com/getgame.php?id=${game_id}`
  );
  const { data: gameData } = await gameRes.json();
  console.log(gameData);
  const gameName = gameData[0].name;
  console.log(gameName);
  return { url, duration, title, gameName };
};

const getStreamerInfo = async (streamer) => {
  const lastGameData = await fetch(`https://decapi.me/twitch/game/${streamer}`);
  const lastGameName = await lastGameData.text();
  console.log(lastGameName);
  const lastGameSrc = `https://static-cdn.jtvnw.net/ttv-boxart/${lastGameName}-144x192.jpg`;
  console.log(lastGameSrc);
  const avatarData = await fetch(`https://decapi.me/twitch/avatar/${streamer}`);
  const avatarSrc = await avatarData.text();
  console.log(avatarSrc);
  return { lastGameName, lastGameSrc, avatarSrc };
};

const dropOptions = (el, opt) => {
  let field = document.getElementById(el);
  $(field).dropdown({
    values: opt,
  });
};
