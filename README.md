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

## Update 08/19/2024:

I have dockerized this application, so now it's even easier to install and run, so: 

## Docker image build and running:

You can now build this docker image and run it like this: 

So, first clone the repo: 

```sh
git clone https://github.com/bask209/SimpleTrackSplitter.git
```

Then, install Docker: 

[Have a read here](https://docs.docker.com/get-docker/)

Once you've got Docker installed, open a terminal and navigate to the folder where you git cloned the repo, then: 

```sh
docker build -t simpletracksplitter .
```

This will create a new image that you can use like this: 

```sh
docker run -p 8501:8501 simpletracksplitter 
```

or

```sh
docker run -p 8501:8501 -d simpletracksplitter 
```

So that way you get your terminal back and this runs detached. 

If everything goes well you should now be able to access the app running in your own computer going to http://localhost:8501/

But we all know that running this kind of things and doing commands and all that is not always going to work... Right? So: 

## Actual easiest way to run this! 

Thanks for getting this far.

In order to run this the easiest way, I've uploaded this image to dockerhub.

This means that as long as you have Docker installed in your computer, you should be able to simply run: 

```sh
docker run -p 8501:8501 -d bask209/simpletracksplitter:latest
```

Then open a web browser and navigate here: 

http://localhost:8501/

This should be working for you now. 

## Update 08/25/2024:

I've realized I want this to get to musicians, tinkerers, people that love to explore music.

So, I will work on tutorials that teach how to run this:

1. Please go to Docker and install Docker Desktop: [Official Docker Documentation](https://docs.docker.com/desktop/install/windows-install/)

    Also a video tutorial (there's a lot on YouTube): [How To Install Docker on Windows? A Step-by-Step Guide](https://www.youtube.com/watch?v=XgRGI0Pw2mM)

    Y también en español: [Docker, Instalación en Windows (más WSL, Window Subsystem for Linux)](https://www.youtube.com/watch?v=ZO4KWQfUBBc) 

2. Now that you have docker desktop installed, you will see something like this: 

    ![alt text](screenshots\DockerDesktopScreen.png)

    You should have no containers, or, just the hello-world container. Now we will look for the image, so we click on the Images button:

     ![alt text](screenshots\DockerDesktopScreenImages.png)

     As you can see at the bottom left, it says the engine is running. This means that now we can open a single terminal command (open the Windows terminal, or Command Prompt from the start menu) and paste the docker command above:

     https://github.com/user-attachments/assets/5e6b222f-82c6-49b9-949b-19f1c8dd25d6

     After this commands finishes running, you'll be able to open any web browser and type http://localhost:8501/ then the app will pop up and you will be able to use it.

     ![image](https://github.com/user-attachments/assets/8e8839bc-2d60-47d1-acd4-79776a5180ad)

     To finish running it, you can just close the Docker engine or hit stop under the Docker Desktop Actions button in the containers tab:

     ![image](https://github.com/user-attachments/assets/5c83fcd4-d816-446f-8f33-75d5a2155ec4)



     



