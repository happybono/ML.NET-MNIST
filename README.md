# ML.NET-MNIST
The ML.NET-MNIST (NumberJangi) project is a C# application that recognizes handwritten digits using a pre-trained ONNX model. The project leverages the Windows InkCanvas for drawing and Microsoft’s Machine Learning libraries for prediction.

<div align="center">
<img alt="GitHub Last Commit" src="https://img.shields.io/github/last-commit/happybono/ML.NET-MNIST"> 
<img alt="GitHub Repo Size" src="https://img.shields.io/github/repo-size/happybono/ML.NET-MNIST">
<img alt="GitHub Repo Languages" src="https://img.shields.io/github/languages/count/happybono/ML.NET-MNIST">
<img alt="GitHub Top Languages" src="https://img.shields.io/github/languages/top/HappyBono/ML.NET-MNIST">
</div>

## What's New
### May 29, 2020
Initial release.

## Features
- Draw digits on the InkCanvas.
- Load an ONNX model for digit recognition.
- Perform real-time digit recognition.
- Display prediction results and confidence scores.

## Requirements
- .NET Framework
- Microsoft.ML.OnnxRuntime
- Windows Machine Learning Code Generator (Extension)

## Getting Started
### Numbers.py
1. Load the solution file in Visual Studio.
2. Go to [ Python Environments ] Window and click on the [ "Add environment" ] button.
3. Click on the [ Existing Enviroment ] tab and set Enviroment to [ torch 3.7 64-bit ].
4. Right-click on the project title and Click on [ Set as StartUp Project ] on the popup menu.
5. Press [ F5 ] to Execute and debug the project.

### Main.cs
1. Right-click on the project title and Click on [ Set as StartUp Project ].
2. Right-click on the project title and Click on [ Manage Nuget Packages... ] on the popup menu.
3. Search for the [ Microsoft.ML.OnnxRuntime ] package and install it.
4. Press [F5] to Execute and debug the project.
5. Follow the instructions shown in the application.

## How It Works
1. **Initialize Components** : The main form initializes and sets up the InkCanvas where the user can draw digits.
2. **Load Model** : An ONNX model is loaded to perform the digit recognition.
3. **Draw Digit** : Users draw digits on the InkCanvas.
4. **Normalize Input** : The drawn digit is captured and normalized by dividing each pixel value by 255.
5. **Predict Digit** : The normalized input is passed to the ONNX model which predicts the digit.
6. **Display Result** : The predicted digit and confidence scores are displayed.

## Code Explanation
### MainForm Initialisation
The constructor initializes the form and the InkCanvas.
```csharp
public Main()
{
    InitializeComponent();
    InitializeCanvas();
}
```

### Prediction
Normalizes the input, performs prediction using the ONNX model, and displays the result.
```csharp
private void Predict(float[] digit)
{
    var x = new DenseTensor<float>(digit.Length);
    for (int i = 0; i < digit.Length; i++)
        x[i] = ((digit[i] / 255) - 0.1307f) / 0.3081f;
    var input = NamedOnnxValue.CreateFromTensor<float>("0", x);
    var output = _session.Run(new[] { input }).First().AsTensor<float>().ToArray();
    var pred = Array.IndexOf(output, output.Max());
    ShowResult(pred, output, 0, Exp);
}
```

### Capture Drawn Digit
Captures the drawn digit from the InkCanvas and prepares it for prediction.
```csharp
private float[] GetWrittenDigit(int size = 28)
{
    RenderTargetBitmap b = new RenderTargetBitmap(
        (int)_inkCanvas.ActualWidth, (int)_inkCanvas.ActualHeight,
        96d, 96d, PixelFormats.Default);
    b.Render(_inkCanvas);
    var bitmap = new WriteableBitmap(b).Resize(size, size, WriteableBitmapExtensions.Interpolation.NearestNeighbor);
    float[] data = new float[size * size];
    for (int x = 0; x < bitmap.PixelWidth; x++)
    {
        for (int y = 0; y < bitmap.PixelHeight; y++)
        {
            var color = bitmap.GetPixel(x, y);
            data[y * bitmap.PixelWidth + x] = 255 - ((color.R + color.G + color.B) / 3);
        }
    }
    return data;
}
```

## Usage
- **Load Model :** Click on the [ Load Model ] button and select an ONNX model file.
- **Draw Digit :** Draw a digit on the InkCanvas.
- **Recognize :** Click on the [ Recognize ] button to predict the drawn digit.
- **Clear :** Click on the [ Clear ] button to clear the canvas and start again.

## Copyright
Copyright ⓒ HappyBono 2020 - 2025. All rights Reserved.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgements
This project references classes from :
[Basic MNIST Example from GitHub (PyTorch)](https://github.com/pytorch/examples/tree/main/mnist)
