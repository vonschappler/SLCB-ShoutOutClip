let evt = new Event('click');

let shoutOut = '';
let body = '';
let profileZone = '';
let profileImg = '';
let streamerInfo = '';
let streamerInfoText = `Check out <%streamer%> (last playing <%game%>)`;
let channelInfo = '';
let channelInfoText = `at <%url%>`;
let gameZone = '';
let gameImg = '';
let clipZone = '';
let clipVideo = '';
let clipInfo = '';
let clipInfoText = `<%clipTitle%> - <%clipGame%>`;
let customStyle = '';
let shoutDuration;

let defaultSettings = {
  animation: 'drop',
  bottomBgColor: '#00ffff',
  bottomTextColor: '#000000',
  clipInfoBgColor: '#000000',
  clipInfoDivider: '#ffff00',
  clipInfoTextColor: '#00ffff',
  clipZoneBorder: '#ffff00',
  displayClip: false,
  displayClipInfo: false,
  imgBgColor: '#ff00ff',
  showClipBorder: false,
  textFont: 'Arial',
  topBgColor: '#ffff00',
  topTextColor: '#00ffff',
  volume: 0.75,
};

$(document).ready(function () {
  if (typeof API_Key === 'undefined') {
    $('body').html(
      'No API Key found<br>Right-click on the script in Streamlabs Chatbot and select "Insert API Key"'
    );
    $('body').css({
      'font-size': '3rem',
      color: '#16b2ab',
      'backround-color': '#1b1c1d',
      'text-align': 'center',
    });
  } else {
    connectWebsocket();
    body = document.querySelector('body');
    shoutOut = document.querySelector('#shoutOut');
    profileZone = document.querySelector('#profileZone');
    profileImg = document.querySelector('#profileImg');
    streamerInfo = document.querySelector('#streamerInfo');
    channelInfo = document.querySelector('#channelInfo');
    gameZone = document.querySelector('#gameZone');
    gameImg = document.querySelector('#gameImg');
    clipZone = document.querySelector('#clipZone');
    clipVideo = document.querySelector('#clipVideo');
    clipInfo = document.querySelector('#clipInfo');
    customStyle = document.querySelector('#customStyle');
    document.dispatchEvent(evt);
  }
});

const connectWebsocket = () => {
  var socket = new WebSocket('ws:127.0.0.1:3337/streamlabs');
  socket.onopen = (message) => {
    var auth = {
      author: 'von_Schappler',
      website: 'http://rebrand.ly/vonWebsite',
      api_key: API_Key,
      events: ['EVENT_SHOUTOUT'],
    };
    socket.send(JSON.stringify(auth));
  };
  socket.onclose = () => {
    socket = null;
    setTimeout(connectWebsocket, 10000);
  };
  socket.onmessage = async (message) => {
    var msg = JSON.parse(message.data);
    if (msg.event == 'EVENT_SHOUTOUT') {
      data = JSON.parse(msg.data);
      const casterName = data['casterName'];
      const clipInfo = data?.['clipInfo'] ?? {};
      const { title: clipTitle, game: clipGame, url: clipUrl } = clipInfo;
      const overlaySettings = data?.['overlaySettings'] ?? {};
      const {
        avatar,
        gameImage,
        lastGame,
        url: casterUrl,
      } = data?.['casterInfo'] ?? {};
      const overlayInfo = {
        avatar,
        casterName,
        lastGame,
        gameImage,
        casterUrl,
        clipUrl,
        clipTitle,
        clipGame,
      };
      const { duration } = clipInfo;
      console.log(overlayInfo);
      document.dispatchEvent(evt);
      const overlayReady = await setOverlayVisuals({
        overlaySettings,
        overlayInfo,
        duration,
      });
      overlayReady && animOverlay({ overlaySettings, shoutDuration });
    }
  };
};

const setOverlayVisuals = async ({
  overlaySettings = defaultSettings,
  overlayInfo = {},
  duration,
}) => {
  customStyle.textContent = `
        @font-face {
          font-family: 'overlayFont';
          src: local("${overlaySettings.textFont}");
        }`;
  $(body).css({
    'font-family': 'overlayFont',
  });
  $(profileZone).css({
    'background-color': overlaySettings.imgBgColor,
  });
  $(streamerInfo).css({
    color: overlaySettings.topTextColor,
    backgroundColor: overlaySettings.topBgColor,
  });
  $(channelInfo).css({
    color: overlaySettings.bottomTextColor,
    backgroundColor: overlaySettings.bottomBgColor,
  });
  $(gameZone).css({
    'background-color': overlaySettings.imgBgColor,
  });
  $(clipZone).css({
    border: `${
      overlaySettings.showClipBorder
        ? `solid 3px ${overlaySettings.clipZoneBorder}`
        : 'none'
    }`,
  });
  profileImg.src = overlayInfo?.avatar;
  streamerInfo.innerHTML = streamerInfoText
    .replace('<%streamer%>', overlayInfo?.casterName)
    .replace('<%game%>', overlayInfo?.lastGame);
  channelInfo.innerHTML = channelInfoText.replace(
    '<%url%>',
    overlayInfo?.casterUrl
  );
  gameImg.src = overlayInfo?.gameImage;
  renderClip({ overlaySettings, overlayInfo, duration });
  return true;
};

const renderClip = ({ overlaySettings, overlayInfo, duration }) => {
  $(clipInfo).css({
    color: overlaySettings.clipInfoTextColor,
    'background-color': overlaySettings.clipInfoBgColor,
    'border-color': overlaySettings.clipInfoDivider,
  });
  clipVideo.src = overlayInfo?.clipUrl;
  clipVideo.volume = overlaySettings.displayClip
    ? overlaySettings.volume / 100
    : 0;
  clipInfo.innerHTML = clipInfoText
    .replace('<%clipTitle%>', overlayInfo.clipTitle)
    .replace('<%clipGame%>', overlayInfo?.clipGame);
  overlaySettings.displayClip
    ? (shoutDuration = duration)
    : (shoutDuration = 10);
  overlaySettings.displayClip
    ? clipZone.classList.remove('hidden')
    : clipZone.classList.add('hidden');
  overlaySettings.displayClipInfo && overlaySettings.displayClip
    ? clipInfo.classList.remove('hidden')
    : clipInfo.classList.add('hidden');
  console.log(clipZone.classList.value);
};

const animOverlay = ({ overlaySettings = defaultStyle, shoutDuration }) => {
  const duration = shoutDuration ?? 10;
  const animIn = `${overlaySettings.animation} in`.toLowerCase();
  const animOut = `${overlaySettings.animation} out.`.toLowerCase();
  duration === 10
    ? clipZone.classList.add('hidden')
    : clipZone.classList.remove('hidden');
  document.dispatchEvent(evt);
  clipVideo.play();
  clipVideo.muted = false;
  $(shoutOut).transition({
    verbose: true,
    animation: animIn,
    duration: '1500ms',
    onComplete: () => {
      $(shoutOut).transition({
        animation: animOut,
        duration: '1500ms',
        interval: (duration - 1) * 1000,
        onComplete: () => {
          clipVideo.muted = true;
          clipVideo.src = '';
        },
      });
    },
  });
};
