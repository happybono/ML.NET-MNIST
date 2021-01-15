# ML.NET-MNIST
This project uses MNIST from PyTorch torchvision dataset to create an ONNX model used to recognize Digits. It also contains a Visual C# Windows Forms Apps project to consume the model.

<div align="center">
<img alt="GitHub Last Commit" src="https://img.shields.io/github/last-commit/happybono/ML.NET-MNIST"> 
<img alt="GitHub Repo Size" src="https://img.shields.io/github/repo-size/happybono/ML.NET-MNIST">
<img alt="GitHub Repo Languages" src="https://img.shields.io/github/languages/count/happybono/ML.NET-MNIST">
<img alt="GitHub Top Languages" src="https://img.shields.io/github/languages/top/HappyBono/ML.NET-MNIST">
</div>

## What's New
### May 29, 2020
Initial release.

## Getting Started
### Numbers.py
1. Load the solution file in Visual Studio.
2. Go to [Python Environments] Window and click on the ["Add environment"] button.
3. Click on the [Existing Enviroment] tab and set Enviroment to [torch 3.7 64-bit].
4. Right Click on the project title and Click on [Set as StartUp Project] on the popup-menu.
5. Press [F5] to Execute and debug the project.

### Main.cs
1. Right Click on the project title and Click on [Set as StartUp Project].
2. Right Click on the project title and Click on [Manage Nuget Packages...] on the popup-menu.
3. Search for the [Microsoft.ML.OnnxRuntime] package and install it.
4. Press [F5] to Execute and debug the project.
5. Follow the instructions shown in an application.

## Copyright / End User License
### Copyright
Copyright ⓒ HappyBono 2019 - 2021. All rights Reserved.

### MIT License
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
