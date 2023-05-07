# 计算机网络 LAB1 实验报告

## 组员： 陈彦伯 张珏 韦贺文

### 源码

- https://github.com/chillanthony/ComNetLab1
- 环境
  - Python 3.11.3
  - MySQL 8.0.32
  - datasky wifi探针


- 文件
  - Server.py 收集Wifi探针发来的数据 解析并插入数据库 
  - Locating.ipynb 用于实验各种定位算法
  - LocatingAlgorithm.py 定位算法的封装版本
  - dataset.csv 从数据库中取出的本实验数据集
  - frontend.html & graph1～4.jpg 前端网页资源
  - 运行./operate.sh 将计算结果展示在浏览器

### 算法解释

- 我们小组将设备放在室内三个不同位置，打开服务器收集并筛选从三个wifi探针发来的信号数据中mac地址为实验设备的数据，对其展开分析。
- 数据选择
  - range
    - wifi探针设备会根据信号强度自动计算range并包含在数据包里。
    - 计算并不准确，在使用range时大多基于三个range比例进行计算。
  - rssi
    - 捕捉到wifi设备发送的信号强度
    - rssi距离转换公式
      - $distance = 10^{(MeasuredPower - RSSI)/10*N}$
      - 经过尝试，我们选择$MeasuredPowwer = -53, N = 3$作为比较合适的参数。

- 数据过滤
  - 由于实体干扰与其他信号干扰，数据中存在噪音。
  - 我们的实验环境为7mx5m，于是我们在数据过滤上简单的采取过滤掉range/distance大于13m的数据。
- 归一化加权
  - 根据三个距离数据的比例，计算三个点坐标在设备坐标中的权值。
  - 注意到权值与距离数据呈反比关系，我们选择函数$f（R）$处理距离数据，并通过公式$W_A = \frac{f(R_A)}{f(R_A)+f(R_B)+f(R_C)}$进行归一化计算出每个路由器坐标在设备坐标中的权值。
  - 经过多次尝试，我们确定$f(R) = 1/R$为误差最小的距离处理函数。
- 几何法求平均
  - ![20200129140458190](/Users/anthony/Desktop/Anthony/Study/计算机网络/LAB1/Ref/计算机网络 LAB1 实验报告.assets/20200129140458190.png)
  - 首先在三边上找出其两端点画出的圆的两交点连线的中点.
    - 计算公式：$PC = PQ/2 + (PA^2 -QA^2)/2PQ$
    - ![20200129142530699-1](/Users/anthony/Desktop/Anthony/Study/计算机网络/LAB1/Ref/计算机网络 LAB1 实验报告.assets/20200129142530699-1.png)
  - 为避免不合法数据影响结果，距离和小于边长和单个距离大于边长的情况均直接采用两边比例直接得到该边上的点。
  - 最后对得到的三个点求重心，得到设备位置的近似值。

### 定位结果

- 算法1: range 归一化方法![graph1](/Users/anthony/Desktop/Anthony/Study/计算机网络/LAB1/Ref/计算机网络 LAB1 实验报告.assets/graph1.jpg)
- 算法2: rssi 归一化方法![graph2](/Users/anthony/Desktop/Anthony/Study/计算机网络/LAB1/Ref/计算机网络 LAB1 实验报告.assets/graph2.jpg)
- 算法3: range 几何法求平均![graph3](/Users/anthony/Desktop/Anthony/Study/计算机网络/LAB1/Ref/计算机网络 LAB1 实验报告.assets/graph3.jpg)
- 算法4: rssi 几何法求平均![graph4](/Users/anthony/Desktop/Anthony/Study/计算机网络/LAB1/Ref/计算机网络 LAB1 实验报告.assets/graph4.jpg)
- 前端截图![Screenshot 2023-05-07 at 23.05.45](/Users/anthony/Desktop/Anthony/Study/计算机网络/LAB1/Ref/计算机网络 LAB1 实验报告.assets/Screenshot 2023-05-07 at 23.05.45.png)

### 结果分析

| Average error | range | rssi |
| ------------- | ----- | ---- |
| 归一化方法    | 1.15  | 1.21 |
| 几何求平均法  | 1.47  | 1.59 |

- 我们可以看到，在相同的算法下，使用range的精确度平均上要稍高于rssi（rssi计算公式已经是校正后的使误差较小的形式）。
- 在本实验中，归一化加权方法的表现要显著优于几何求平均法，我们认为原因如下
  - 归一化加权是一种较为粗略的方法，没有几何上的精确性，但却能够由于权值计算函数的灵活性在实验场景特定的情况下实现较高的精确度。
  - 几何法在实验数据合法性较高的情况下具有较高的准确度，然而，在本实验中，由于实验数据的限制，首先在三角形边上求点时需要为了处理不合法数据引入比例方法，其次，在根据三个边上点求设备坐标时，为了计算形式的简便采取了直接计算重心，也导致了一定的误差，使得我们的几何法实质上也成为了一种不成功的近似算法。
  - 如果扩大实验数据集，并且在原始数据处理上使得用于计算坐标的数据更为合法（例如拟合距离-range对应关系函数）并改进几何法，相信会在精确性上有更好的表现。

