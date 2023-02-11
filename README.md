# GPTerm

Interact and chat with OpenAI's GPT-3 models via an REPL terminal emulation on macOS.
Including voiced output, image generation and model selection.

<br>

<img width="640" alt="gpterm" src="https://user-images.githubusercontent.com/125149025/219539378-2dad2363-a3bf-4335-ba4a-201bb1622951.png">

## Installation

To install GPTerm, simply execute the following command in your terminal:

```sh
pip3 install --upgrade gpterm
```

> **_Note:_** GPTerm works best when installed and run under a [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) environment. See [Known Issues](#known-issues)
> 
> To install under conda (after installing anaconda or miniconda):
> ```sh
> conda create --name gpterm python=3.10.8
> conda activate gpterm
> pip3 install --upgrade gpterm
> ```

## Usage

```sh 
gpterm
```

> **_Note:_** GPTerm uses the OpenAI API which requires an [OpenAI API Key](https://platform.openai.com/account/api-keys)
>

* **Setting an OpenAI API Key:** 
  
  You can get your OpenAI API Key from [OpenAI](https://platform.openai.com/account/api-keys)

  Storing it in the file `~/.openai-api-key` will allow to run GPTerm without manually providing it with the API key. 
  In the command below replace **api_key** with your OpenAI API Key.

  <pre>
  echo <b>api_key</b> > ~/.openai-api-key
  </pre>

  Alternatively, you can provide your API Key to `gpterm` by passing it with one of these flags: 

  `--api_key <api_key>`

  `--api_key_path <path/to/file/containing/api_key>`
  
  Or by setting a shell environment variable `OPENAI_API_KEY` with your API Key before running `gpterm`

  <br>

* **Setting the Color Theme:**

  For the best experience a terminal with a **dark** background theme is recommended. (*Like the one provided by [iTerm](https://iterm2.com/)*)
  
  However, if you are using a light background terminal start gpterm with the following flag:

  `--theme light`

  *Options are **light** or **dark** (default)*

### Features

GPTerm provides the following features as supported by OpenAI's API:

* Streamed output
* Multiline input
* Preserves conversation context including the option to reset it
* Voiced output using text to speech (with a variety of voices to choose from)
* Image Generation using a DALL·E model (*note that as the saying goes an image is worth a thousand tokens...*)
* Model-3 selection and parameters
* Displays number of remaining tokens for current conversation context before it is reset (Due to `max_tokens` limited by OpenAI's API)
* Code blocks formatted with Syntax highlighting (experimental)



### Known Issues

* Tab completion doesn't seem to work well in the **readline** module that comes with native python. The [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) environment includes a python binary with a readline module that does support it.

