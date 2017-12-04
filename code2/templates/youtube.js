
    var c = 1;
    var buttonState = "NONE"; // PLAY, PAUSE, STOP
    var playerState;

    var startCapture;
    /// var stopCapture;
    // var isStartCapture = false;

    $('div').on('mouseover', function() {
        //console.log('mouseover');

        $('.isHover').html('in');
    });

    $('div').on('mouseout', function() {
        //console.log('mouseout');
        $('.isHover').html('out');
    });

    $('div').on('mousemove', function() {
        $('.isHover').html(c++);
    });

    /**
     * Youtube API 로드
     */
     var tag = document.createElement('script');
    tag.src = "http://www.youtube.com/iframe_api";
    var firstScriptTag = document.getElementsByTagName('script')[0];
    firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

    /**
     * onYouTubeIframeAPIReady 함수는 필수로 구현해야 한다.
     * 플레이어 API에 대한 JavaScript 다운로드 완료 시 API가 이 함수 호출한>다.
     * 페이지 로드 시 표시할 플레이어 개체를 만들어야 한다.
     */
    var player;
    function onYouTubeIframeAPIReady() {
        player = new YT.Player('youtube', {
            height: '315',            // <iframe> 태그 지정시 필요없음
            width: '560',             // <iframe> 태그 지정시 필요없음
            videoId: '9bZkp7q19f0',   // <iframe> 태그 지정시 필요없음
            playerVars: {             // <iframe> 태그 지정시 필요없음
                controls: '2'
            },
            events: {
                'onReady': onPlayerReady,               // 플레이어 로드가 >완료되고 API 호출을 받을 준비가 될 때마다 실행
                'onStateChange': onPlayerStateChange    // 플레이어의 상태가 변경될 때마다 실행
            }
        });
    }
    function onPlayerReady(event) {
        console.log('onPlayerReady 실행');
    }

    function onPlayerStateChange(event) {
        playerState = event.data == YT.PlayerState.ENDED ? '종료됨' :
                event.data == YT.PlayerState.PLAYING ? '재생 중' :
                event.data == YT.PlayerState.PAUSED ? '일시중지 됨' :
                event.data == YT.PlayerState.BUFFERING ? '버퍼링 중' :
                event.data == YT.PlayerState.CUED ? '재생준비 완료됨' :
                event.data == -1 ? '시작되지 않음' : '예외';

        console.log('onPlayerStateChange 실행: ' + playerState + " btn: " + buttonState);
        printPlayerState();
        printButtonState();

        if (playerState == '재생 중') {


        }
        else if (playerState == '일시중지 됨') {

        }
        else {
        }

        // 재생여부를 통계로 쌓는다.
        collectPlayCount(event.data);
    }


    stopCapture = function() {
        clearInterval(startCapture);
    }
     function printPlayerState() {
        var element = document.getElementById("playerState");
        element.innerHTML = playerState;
    }

    function printButtonState() {
        var e = document.getElementById("buttonState");
        e.innerHTML = buttonState;
    }

    function playYoutube() {
        // 플레이어 자동실행 (주의: 모바일에서는 자동실행되지 않음)
        buttonState = "PLAY"
        player.playVideo();
        //startCapture();
    }
    function pauseYoutube() {
        buttonState = "PAUSE"
        player.pauseVideo();
        //clearInterval(startCapture);

    }
    function stopYoutube() {
        buttonState = "STOP"
        player.seekTo(0, true);     // 영상의 시간을 0초로 이동시킨다.
        player.stopVideo();
    }
    var played = false;
    function collectPlayCount(data) {
        if (data == YT.PlayerState.PLAYING && played == false) {
            // todo statistics
            played = true;
            console.log('statistics');
        }
    }

    function startCapture() {
        startCapture = setInterval(
            function myFunction(x) {
                $.getJSON('/captureUserFace', {post: playerState},
                    function(data) {
                        var faces = data.result;
                        console.log('python response : ' + faces);
                    }
                );
        }, 3000 );
    };