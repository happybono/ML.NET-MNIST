# ML.NET-MNIST
This project uses MNIST from the PyTorch torchvision dataset to create an ONNX training model used to recognize handwriting digits. This also contains a Visual C# Windows Forms Apps project to consume the model.

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

## Copyright
Copyright ⓒ HappyBono 2021 - 2025. All rights Reserved.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.
