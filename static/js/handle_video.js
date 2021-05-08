console.log('Called Video Handler')

var video_element = document.getElementById("stream_video")
console.log(screen.width)
if (screen.width < 1280 ) {
    console.log("For small screen ");
	video_element.width = screen.availWidth;
	video_element.height = screen.availWidth;
}
