function showImg(input) {
	if (input.files && input.files[0]) {
	  var reader = new FileReader();
	  reader.onload = function(e) {
		document.getElementById('bg03-02-preview').src = e.target.result;
	  };
	  reader.readAsDataURL(input.files[0]);
	} else {
	  document.getElementById('bg03-02-preview').src = "";
	}
};
function myFunction(msg) {
	alert(msg);
}

console.log('test');