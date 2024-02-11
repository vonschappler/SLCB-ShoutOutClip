const elemFontsSelect = document.getElementById('fontSelector');
const elemFontInfo = document.getElementById('font-info');
const elemFontInfoFullName = document.getElementById('font-info-full-name');
const elemFontInfoStyle = document.getElementById('font-info-style');
const elemFontStyle = document.getElementById('font-style');
const fontMap = new Map();
let enabled = true;

const showStatus = async () => {
  if (!self.queryLocalFonts) {
    alert('API is not available on this platform.');
    enabled = false;
    return;
  }
};

const loadFonts = async () => {
  if (!enabled) {
    $('#msgInfo').removeClass('warning');
    $('#msgInfo').addClass('error');
    $('#msgHeader').html('Error:');
    $('#msgContent').html(
      'Please be sure to use a browser with queryLocalFonts capability.'
    );
    return;
  }
  try {
    reset();
    let fonts;
    fonts = await self.queryLocalFonts();
    if (fonts.length === 0) {
      elemFontsSelect[0] = new Option('No fonts returned', '');
      $('#msgInfo').removeClass('warning success hidden');
      $('#msgInfo').addClass('error visible');
      $('#msgHeader').html('Error:');
      $('#msgContent').html(
        'Please allow the application to search for fonts on your computer.'
      );
      setTimeout(() => {
        $('#msgInfo').removeClass('erro success hidden');
        $('#msgInfo').addClass('warning visible');
        $('#msgHeader').html('Attention!');
        $('#msgContent').html(
          `To enable font preview in the overlay, some permissions must be granted to this page. To grant the necessary permissions, click <a href='#' onclick="loadFonts()">here</a>.`
        );
      }, 5000);
      return;
    }
    $('#msgInfo').removeClass('warning error hidden');
    $('#msgInfo').addClass('success');
    $('#msgHeader').html('Congratulations!');
    $('#msgContent').html(
      `Fonts are now selectable for previewing on the overlay.`
    );
    setTimeout(() => {
      $('#msgInfo').removeClass('visible');
      $('#msgInfo').addClass('hidden');
    }, 5000);
    elemFontsSelect[0] = new Option('Select a font to preview', '');
    fonts.forEach((font, index) => {
      fontMap.set(font.postscriptName, font);
      elemFontsSelect.append(new Option(font.fullName, font.postscriptName));
    });
  } catch (e) {
    elemFontsSelect[0] = new Option(`Cannont query fonts: ${e.message}`, '');
  }
};

const reset = () => {
  fontMap.clear();
  elemFontInfo.style.display = 'none';
  elemFontInfoFullName.innerText = '';
  elemFontInfoStyle.innerText = '';
};

const onFontSelected = async () => {
  if (elemFontsSelect.value === '') {
    reset();
    return;
  }
  const selectedFontData = fontMap.get(elemFontsSelect.value);
  if (selectedFontData) {
    elemFontStyle.textContent = `
        @font-face {
          font-family: "dynamic-font";
          src: local("${selectedFontData.postscriptName}");
        }`;
    elemFontInfoFullName.innerText = `Full Name: ${selectedFontData.fullName}`;
    elemFontInfoStyle.innerText = `Style: ${selectedFontData.style}`;
    elemFontInfo.style.fontFamily = 'dynamic-font';
    elemFontInfo.style.display = 'inline-block';
  } else {
    elemFontInfoFullName.innerText = 'Unable to load font data';
  }
};
