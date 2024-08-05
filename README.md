# SimpleTrackSplitter

As the name states... This is a simple track splitter. It uses project demucs as the splitting engine. 

I was using StemRoller before, but I also wanted to convert some songs that weren't hosted on YouTube, so I started using Demucs, then I decided to make my own thing. 

It's pretty simple: 

1. It downloads the audio from a YouTube video. 
2. Audio gets separated into tracks using demucs.

On the first point I can also change the source and use any audio file to pass it to Demucs. 

I'm using the default demucs settings, but the way it's laid out, it allows for a lot of customization on it. 

I'll probably end up creating a streamlit app, and dockerizing it so anyone can run it. 

It does use pytorch and will benefit a lot from CUDA accelerated calculations. 

Have a look at Demucs documentation first: 

[Demucs Github](https://github.com/adefossez/demucs)

## Installation: 

Welp. Here's where it gets nasty. This is one of the first iterations of this, so hopefully I'll make this a better process for users.

At the moment, you need to have python installed, 3.8+ will work, I've done extensive testing with 3.10.7, so:

1. We'll do a package installation first. Do you want to set up your virtual environment? 

    ```bash
    python -m venv .venv
    ```

2. Don't forget to activate the virtual environment. 

    ```bash
    .\.venv\Scripts\activate 
    ```

3. Now, within that environment, we'll do the regular pytorch installation:

    ```bash
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
    ```

    This is the one that works for my GPU. Please check out your GPUs CUDA version... I mean, have a look here: [Pytorch official installation documentation](https://pytorch.org/get-started/locally/), because they know what they're doing.

    You can also use a CPU to run this model, but... You'll have to be patient.

    Now for the rest of the packages: 

    ```bash
    pip install -r requirements.txt
    ```

    You can install the requirements by yourself, it's not much, have a look at the dependencies. Nowadays Numpy is on a newer version, that's why I specified numpy 1.26.4. This will probably happen for other dependencies in the future, so I'll leave a list of the ones installed right now in another txt file. If you also know what you're doing, you know that you can do: 

    ```bash
    pip install -r freeze.txt
    ```

    Instead of the other one. Options! I like having options.

4. You should have installed ffmpeg. Since this **will work different for different OS**, be patient, read on how to install ffmpeg on your own. Also, some OS support pyaudio as a backend to convert audio files, so, maybe you're lucky and you won't need ffmpeg. 

    At the time I'm writing this, I am running on Windows 11, I have ffmpeg on my path directory, but, sure enough, I had to copy the ffmpeg.exe, ffplay.exe and ffprobe.exe to my root directoy so this could work. Windows works in mysterious ways.

4. Docker container is coming soon, so you can run this anywhere. Anywhere with enough resources at least.

## How to use it?

Well, at this stage, just hop into the *youtube_separate.py* file and change the link on line 24. If you don't know what you're doing, try and maintain the same format of the file. If that fails, shoot me a message, I'll try to reply.

After changing the link you can run the app.

Don't forget to activate your virtual environment **before doing anything**.