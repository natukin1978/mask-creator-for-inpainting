# Mask Creator For Inpainting

![png](./images/outline.png)

Mask Creator For Inpainting is a tool to create inpaint mask images for Stable Diffusion WebUI (Automatic1111). The tool detects the face area in the input image and generates a mask image with the face area white and the rest of the image black.

## Requirements

* OpenCV
* NumPy

## Installation

Go to project directory and install the module.
```
python -m pip install -r requirements.txt
```

Download and save the following files at the first startup.

https://raw.githubusercontent.com/nagadomi/lbpcascade_animeface/master/lbpcascade_animeface.xml

This cascade file is good at detecting anime faces.
You can use `haarcascade_frontalface_default.xml` if you prefer live action.

## Usage

```
python mask_creator.py (image files folder)
```

It is better to enclose the path in double quotes, as it will be cut off if the path contains spaces.

Example.
```
python mask_creator.py "C:\stable-diffusion-webui\outputs\txt2img-images\sample"
```

A subfolder `mask_inpaint_face` is created and the mask image is generated there.


There is also a tool that overlays an image with a mask.

```
python mask_overlay.py (image files folder)
```

A window will appear and overlay the image with a semi-transparent mask.

Use the left and right arrow keys on your keyboard to switch between images.

If the face recognition does not work well and the mask position is bad, press the "Del" key on the keyboard to mark it as "Skip".

(Rest assured that your files will not be deleted.)

You will be asked if the marked image and mask should be moved when exiting the tool.

If you move it, a subfolder called "Skip" will be created in the same place as the image folder,
and the image and mask will be moved there.

## Contributing

If you would like to contribute to Mask Creator For Inpainting, please open an issue to discuss your ideas or submit a pull request.

## Author

ナツキソ

- Twitter: [@natukin1978iai](https://twitter.com/natukin1978iai)
- Mastodon: [@natukin1978iai@pawoo.net](https://pawoo.net/web/accounts/2199670)
- GitHub: [@natukin1978](https://github.com/natukin1978)
- Mail: natukin1978@hotmail.com

## License

Mask Creator For Inpainting is released under the [MIT License](https://opensource.org/licenses/MIT).
