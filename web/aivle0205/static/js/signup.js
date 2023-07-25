function openPopup(event) {
  event.preventDefault();
  var popupURL = this.getAttribute('href');

  var width = 720;
  var height = 170;
  var left = (window.innerWidth - width) / 2;
  var top = (window.innerHeight - height) / 2;

  var popupWindow = window.open(
    popupURL,
    '인증 팝업',
    'width=' + width + ',height=' + height + ',left=' + left + ',top=' + top
  );

  // 팝업 창이 닫히면서 인증이 완료되었을 때 처리
  function handlePopupClose(event) {
    if (event.data === '인증 완료') {
      window.location.href = '/accounts/signup/';
      // 추가 작업 수행 또는 페이지 이동 등 필요한 동작 수행
    }
    // 이벤트 리스너 해제
    window.removeEventListener('message', handlePopupClose);
  }

  // 팝업 창이 닫히는 이벤트를 감지하여 처리
  window.addEventListener('message', handlePopupClose);

  // 부모 창에 팝업 창 객체 전달 (옵션이지만 일부 브라우저에서 필요할 수 있음)
  popupWindow.opener = window;
}
