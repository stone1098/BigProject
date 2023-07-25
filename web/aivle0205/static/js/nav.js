function myFunction(msg) {
	alert(msg);
}

function jumpToID(e, id) {
	let NAVHEIGHT = 40;
	let topofElement = document.getElementById(id).offsetTop - NAVHEIGHT;
	window.scroll({
		top: topofElement,
		behavior: "smooth"
	});
	e.preventDefault();
}

function jumpToFoot(e, id) {
	let bottomofElement = document.getElementById(id).offsetTop + document.getElementById(id).offsetHeight;
	let windowHeight = window.innerHeight;
	let scrollHeight = document.documentElement.scrollHeight;
	let scrollTo = Math.max(bottomofElement - windowHeight, scrollHeight - windowHeight);
	window.scroll({
	  top: scrollTo,
	  behavior: "smooth"
	});
	e.preventDefault();
  }

window.addEventListener('DOMContentLoaded', event => {

	// var nav = document.querySelector('nav');
	// var navitem = document.querySelector('.nav-item');
	// nav.addEventListener('mouseenter', function () {
	// 	navitem.classList.add('nav-hover');
	// });
	// nav.addEventListener('mouseleave', function () {
	// 	navitem.classList.remove('nav-hover');
	// });

	var container = document.querySelector('#container01');
    var nav = document.querySelector('nav');

    container.addEventListener('mouseenter', function () {
        nav.classList.add('nav-hover');
    });

    container.addEventListener('mouseleave', function () {
        nav.classList.remove('nav-hover');
    });

	let navbarShrink = function (){
		const navbarComp = document.body.querySelector('#mainnav');
		if (!navbarComp){
			return;
		}
		
		if (window.scrollY === 0) {
			navbarComp.classList.remove('navbar-shrink');
		} else {
			navbarComp.classList.add('navbar-shrink');
		}
	};
	navbarShrink();
	document.addEventListener('scroll', navbarShrink);
})

function switchPannel(e, direction) {
	const pannelList = [
		".board",
		".contact"
	]
	let currentPannels = document.body.querySelectorAll('#support .active-pannel');
	let idx = parseInt(currentPannels[0].dataset.idx) + parseInt(direction);
	if (idx == pannelList.length) {
		idx = 0
	} else if (idx < 0) {
		idx = pannelList.length - 1;
	}
	nextPannels = document.body.querySelectorAll(pannelList[idx]);

	currentPannels.forEach((element)=>{
		element.classList.remove('active-pannel');
	});
	nextPannels.forEach((element)=>{
		element.classList.add('active-pannel');
	});
	e.preventDefault();
}

function goPrivacy(event) {
	event.preventDefault();  // 링크 클릭 시 기본 동작(페이지 이동)을 막음
	// 팝업 창 열기
	window.open('/test/', '_blank', 'width=600,height=500,scrollbars=yes');
}