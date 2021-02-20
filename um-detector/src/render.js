//import Recorder from 'opus-recorder-master';

document.addEventListener('DOMContentLoaded', function() {
    var URL = chrome.runtime.getURL("popup.html");//window.URL || window.webkitURL;
    console.log(URL);
  
    var gumStream; 						//stream from getUserMedia()
    var rec; 							//Recorder.js object
    var input; 							//MediaStreamAudioSourceNode we'll be recording
  
    // shim for AudioContext when it's not avb.
    var AudioContext = window.AudioContext || window.webkitAudioContext;
    var audioContext; //audio context to help us record
  
    var recordButton = document.getElementById("record");
    var stopButton = document.getElementById("stop");
    //var closeButton = document.getElementById("download");
    //var pauseButton = document.getElementById("pause");
  
    var recorderStop = function(){ rec.stop(); };
  
    //add events to those 2 buttons
    recordButton.addEventListener("click", startRecording);
    stopButton.addEventListener("click", stopRecording);
    stopButton.addEventListener("click", recorderStop);
  
    //pauseButton.addEventListener("click", pauseRecording);
  
    function startRecording() {
        console.log("recordButton clicked");
  
        /*
            Simple constraints object, for more advanced audio features see
            https://addpipe.com/blog/audio-constraints-getusermedia/
        */
  
        var constraints = { audio: true, video:false };
  
         /*
            Disable the record button until we get a success or fail from getUserMedia()
        */
  
        recordButton.disabled = true;
        stopButton.disabled = false;
        //pauseButton.disabled = false;
  
        /*
            We're using the standard promise based getUserMedia()
            https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia
        */
      console.log(navigator.mediaDevices.getUserMedia(constraints));
        navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
            console.log("getUserMedia() success, stream created, initializing Recorder.js ...");
  
            /*
                create an audio context after getUserMedia is called
                sampleRate might change after getUserMedia is called, like it does on macOS when recording through AirPods
                the sampleRate defaults to the one set in your OS for your playback device
  
            */
            audioContext = new AudioContext();
  
            //update the format
            document.getElementById("formats").innerHTML="Format: 1 channel pcm @ "+audioContext.sampleRate/1000+"kHz";
  
            /*  assign to gumStream for later use  */
            gumStream = stream;
        console.log(gumStream);
  
            /* use the stream */
            input = audioContext.createMediaStreamSource(stream);
  
            /*
                Create the Recorder object and configure to record mono sound (1 channel)
                Recording 2 channels  will double the file size
            */
            rec = new Recorder(input,{numChannels:1});
        console.log(rec);
            //start the recording process
            rec.start();
  
            console.log("Recording started");
  
        }).catch(function(err) {
              //enable the record button if getUserMedia() fails
            recordButton.disabled = false;
            stopButton.disabled = true;
                console.log(err);
            //pauseButton.disabled = true;
        });
    }
    /*
    function pauseRecording(){
        console.log("pauseButton clicked rec.recording=",rec.recording );
        if (rec.recording){
            //pause
            rec.stop();
            pauseButton.innerHTML="Resume";
        }else{
            //resume
            rec.record();
            pauseButton.innerHTML="Pause";
  
        }
    }
    */
    function stopRecording() {
        console.log("stopButton clicked");
  
        //disable the stop button, enable the record too allow for new recordings
        stopButton.disabled = true;
        recordButton.disabled = false;
        //pauseButton.disabled = true;
  
        //reset button just in case the recording is stopped while paused
        //pauseButton.innerHTML="Pause";
  
        //tell the recorder to stop the recording
        rec.stop();
  
        //stop microphone access
        gumStream.getAudioTracks()[0].stop();
  
        //create the wav blob and pass it on to createDownloadLink
        //rec.exportWAV(createDownloadLink);
      //rec.ondataavailable(gumstream);
      ondataavailable(gumStream);
      //createDownloadLink();
    }
  
  
    function createDownloadLink(blob) {
        recordingsList = document.getElementById('recordingsList');
  
        var url = URL.createObjectURL(blob);
        var au = document.createElement('audio');
        var li = document.createElement('li');
        var link = document.createElement('a');
  
        //name of .wav file to use during upload and download (without extendion)
        var filename = new Date().toISOString();
  
        //add controls to the <audio> element
        au.controls = true;
        au.src = url;
  
        //save to disk link
        link.href = url;
        link.download = filename+".wav"; //download forces the browser to donwload the file using the  filename
        link.innerHTML = "Save to disk";
  
        //add the new audio element to li
        li.appendChild(au);
  
        //add the filename to the li
        li.appendChild(document.createTextNode(filename+".wav "));
  
        //add the save to disk link to li
        li.appendChild(link);
  
        //upload link
        var upload = document.createElement('a');
        upload.href="#";
        upload.innerHTML = "Upload";
        upload.addEventListener("click", function(event){
              var xhr=new XMLHttpRequest();
              xhr.onload=function(e) {
                  if(this.readyState === 4) {
                      console.log("Server returned: ",e.target.responseText);
                  }
              };
              var fd=new FormData();
              fd.append("audio_data",blob, filename);
              xhr.open("POST","upload.php",true);
              xhr.send(fd);
        });
        li.appendChild(document.createTextNode (" "));//add a space in between
        li.appendChild(upload);//add the upload link to li
  
        //add the li element to the ol
        recordingsList.appendChild(li);
    }
  
    console.log(rec);
    var ondataavailable = function( typedArray ){
      console.log('Data received');
      var dataBlob = new Blob( [typedArray], { type: 'audio/wav' } );
      var fileName = new Date().toISOString() + ".wav";
      console.log(dataBlob);
      console.log(fileName);
      var url = window.URL.createObjectURL( dataBlob );
  
      var audio = document.createElement('audio');
      audio.controls = true;
      audio.src = url;
  
      var link = document.createElement('a');
      link.href = url;
      link.download = fileName;
      link.innerHTML = link.download;
  
      var li = document.createElement('li');
      li.appendChild(link);
      li.appendChild(audio);
  
      recordingsList.appendChild(li);
    };
  
  }, false);
  

/* const { desktopCapturer, remote } = require('electron');
const { writeFile } = require('fs');
const { dialog, Menu } = remote;

// recording
let mediaRecorder;
const recordedChunks = [];

// Buttons
const videoElement = document.querySelector('video');
const startButton = document.getElementById('startButton');
const stopButton = document.getElementById('stopButton');
const getAudioButton = document.getElementById('getAudioButton');

startButton.onclick = e => {
    if (mediaRecorder == null) {
        console.log('get audio source first!');
        return;
    }
    mediaRecorder.start();
    startButton.classList.add('is-danger');
    startButton.innerText = 'Recording'
}

stopButton.onclick = e => {
    mediaRecorder.stop();
    startButton.classList.remove('is-danger');
    startButton.innerText = 'Start';
}

getAudioButton.onclick = getAudioSources;

// get video sources
async function getAudioSources() {
    // const inputSources = await desktopCapturer.getSources({
    //     types: ['window', 'screen']
    // });
    selectSource();
    // const videoOptionsMenu = Menu.buildFromTemplate(
    //     inputSources.map(source => {
    //         return {
    //             label: source.name,
    //             click: () => selectSource(source)
    //         };
    //     })
    // );
    // videoOptionsMenu.popup();
}

async function selectSource() {
    //  getAudioButton.innerText = source.name;

    const constraints = {
        audio: {
            mandatory: {
                chromeMediaSource: 'desktop'
            }
        },
        video: false
    }
    // create a stream
    const stream = await navigator.mediaDevices.getUserMedia(constraints);
    const audioContext = new AudioContext();
    const input = audioContext.createMediaStreamSource(stream);
    const options = { mimeType: 'audio/wav; codecs=vp9' };
    mediaRecorder = new MediaRecorder(stream, options);


    // show preview in a video element
    // videoElement.srcObject = stream;
    // videoElement.play();

    // create media recorder
    // const options = { mimeType: 'audio/wav; codecs=vp9' };
    //  mediaRecorder = new MediaRecorder(stream, options);

    // register event handlers
    mediaRecorder.ondataavailable = handleDataAvailable;
    mediaRecorder.onstop = handleStop;

}

function handleDataAvailable(e) {
    console.log('video data available');
    recordedChunks.push(e.data);
}

async function handleStop(e) {
    const blob = new Blob(recordedChunks, {
        type: 'audio/wav; codecs-vp9'
    });
    const buffer = Buffer.from(await blob.arrayBuffer());
    const { filePath } = await dialog.showSaveDialog({
        buttonLabel: 'Save Recording',
        defaultPath: `um-detector-${Date.now()}.wav`
    });

    console.log(filePath);

    writeFile(filePath, buffer, () => console.log('audio saved successfully'));

} */