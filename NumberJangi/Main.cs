/* 
 * ----------------------------------------------------------------------------------------
 *  NumberSage :: happybono@outlook.com (HappyBono)
 * ----------------------------------------------------------------------------------------
 * 
 *  Presented On   http://www.happybono.net/
 *  C# .NET 사용자들을 위한 MNIST 손글씨 인식 예시 소스 코딩 자료.
 * 
 *  Copyright (R) 2018 - 2022.          
 * 
 *  =======================================================================================
 * 
 *  외부 라이브러리에서 몇 가지 클래스를 참고하여 사용하였습니다.
 *  다음은 그 클래스 목록입니다.:
 * 
 *  Basic MNIST Example from GitHub, January, 2019 (Copyright by PyTorch). 
 *  https://github.com/pytorch/examples/tree/master/mnist 
 */

   
using System;
using System.IO;
using System.Windows.Ink;
using System.Windows.Forms;
using System.Windows.Controls;
using System.Windows.Media.Imaging;
using System.Windows.Media;
using System.Text;

// Allows you to load up .onnx files and executes them.
// .onnx 형식의 파일을 불러오고 실행 가능하도록 해 주는 네임스페이스입니다.

// Go to Extensions - Manage Extensions, then install [Windows Machine Learning Code Generator].  
// [확장] - [확장 관리] 로 진입하신 후 [Windows Machine Learning Code Generator] 패키지를 검색하여 설치하세요.
using Microsoft.ML.OnnxRuntime;

using System.Numerics.Tensors;
using System.Collections.Generic;
using System.Linq;
using static System.Math;

namespace NumberSage
{
    public partial class Main : Form
    {
        private InkCanvas _inkCanvas;
        public Main()
        {
            InitializeComponent();
            InitializeCanvas();
        }

        private void Predict(float[] digit)
        {
            try
            {
                // New data type called "Tensor" in .NET.
                // .NET 에 "Tensor" 라는 데이터 타입이 새롭게 추가되었습니다.
                var x = new DenseTensor<float>(digit.Length);

                for (int i = 0; i < digit.Length; i++)

                    /* Divide by 255 to get the darkest color in the canvas (Normalization).
                       255 로 나누어 캔버스 안에 쓰여진 색상 중 가장 어두운 (명확한) 색상을 구분합니다. 

                       x[i] = ((digit[i] / 255) - Transforms.Normalize(0.1307,), (0.3081,))
                       https://pytorch.org/docs/stable/torchvision/transforms.html#torchvision.transforms.Normalize */
                    x[i] = ((digit[i] / 255) - 0.1307f) / 0.3081f;

                var input = NamedOnnxValue.CreateFromTensor<float>("0", x);            
                var output = _session.Run(new[] { input }).First().AsTensor<float>().ToArray();

                // Performs prediction on an array.
                // 배열 (Array) 에 대해 예측합니다.
                var pred = Array.IndexOf(output, output.Max());

                // Outputs predicted score using Lambda Expression.  
                // 배열에 대해 람다 구문을 통해 예측한 적중률을 출력합니다.
                ShowResult(pred, output, 0, Exp); // ShowResult(pred, output, 0, v => System.Math.Exp(v))
            }

            catch
            {
                MessageBox.Show("Load model file to recognize handwriting.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private InferenceSession _session;
        private void LoadModel(string file)
        {
            // Data Model Added Successfully!
            // 데이터 모델 파일 불러오기 완료!
            _session = new InferenceSession(file);

            toolStripStatusLabel1.Text = "Write any numbers between 1 ~ 9 and click the [Recognize] button.";
        }

        private float[] GetWrittenDigit(int size = 28)
        {
            RenderTargetBitmap b = new RenderTargetBitmap(
                (int)_inkCanvas.ActualWidth, (int)_inkCanvas.ActualHeight,
                96d, 96d, PixelFormats.Default);

            b.Render(_inkCanvas);
            var bitmap = new WriteableBitmap(b)
                            .Resize(size, size, WriteableBitmapExtensions.Interpolation.NearestNeighbor);

            float[] data = new float[size * size];
            for (int x = 0; x < bitmap.PixelWidth; x++)
            {
                for (int y = 0; y < bitmap.PixelHeight; y++)
                {
                    var color = bitmap.GetPixel(x, y);
                    data[y * bitmap.PixelWidth + x] = 255 - ((color.R + color.G + color.B) / 3);
                }
            }

            Console.WriteLine(Stringify(data));
            return data;
        }

        private string Stringify(float[] data)
        {
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < data.Length; i++)
            {
                if (i == 0) sb.Append("{\r\n\t");
                else if (i % 28 == 0)
                    sb.Append("\r\n\t");
                sb.Append($"{data[i],3:##0}, ");

            }
            sb.Append("\r\n}\r\n");
            return sb.ToString();
        }

        private void ShowResult(int prediction, float[] scores, double time, Func<double, double> conversion = null)
        {
            StringBuilder sb = new StringBuilder();
            sb.AppendLine("Scores:");

            for (int i = 0; i < scores.Length; i++)
            {
                double v = conversion == null ? scores[i] : conversion(scores[i]);
                sb.AppendLine($"\t{i}: {v}");
            }

            sb.AppendLine($"Prediction: {prediction}");
            sb.AppendLine($"Time: {time}");
            labelPrediction.Text = prediction.ToString();

            textResponse.Text = "";
            textResponse.Text = sb.ToString();
        }

        private void Clear()
        {
            _inkCanvas.Strokes.Clear();
            textResponse.Clear();
            labelPrediction.Text = "";
        }

        private void InitializeCanvas()
        {            
            _inkCanvas = new InkCanvas();
            _inkCanvas.DefaultDrawingAttributes = new DrawingAttributes()
            {
                FitToCurve = true,
                Height = 16,
                Width = 16
            };
            hostCanvas.Child = _inkCanvas;
            labelPrediction.Text = "";
        }

        private void buttonRecognize_Click(object sender, EventArgs e)
        {
            if (_inkCanvas.Strokes.Count == 0)
            {
                MessageBox.Show("Sorry, you must write on the canvas to recognize handwriting.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
            else
            {
                Predict(GetWrittenDigit());
            }
        }

        private void buttonClear_Click(object sender, EventArgs e)
        {
            Clear();
        }

        private void buttonLoad_Click(object sender, EventArgs e)
        {
            if(openFile.ShowDialog() == DialogResult.OK && File.Exists(openFile.FileName))
                LoadModel(openFile.FileName);
        }
    }
}
