#include "python2.7/Python.h"
#include <stdlib.h>
#include <math.h>

//辅助函数
float S(float val) {
    float x = fabs(val);

    if (x >= 0 && x < 1) {
        return (1 - 2*x*x +x*x*x);
    }
    else if (x >= 1 && x < 2) {
        return (4 - 8*x + 5*x*x - x*x*x);
    }
    else {
        return 0;
    }
}

//双线性内插值
int linear(int v1, int v2, int v3, int v4, float p, float q) {
    int result = v1*(1.0-p)*(1.0-q) + v2*p*(1-q) + v3*(1-p)*q + v4*p*q;

    return result;
}
//三次卷积法 p 是x 方向的 q 是y方向
int cubic(int ** vals, float p, float q) {
    int result, i;
    float * tmpArr = malloc(sizeof(int)*4);
    //三次卷积内差值法公式
    for (i=0; i < 4; i++) {
        tmpArr[i] = S(p+1)*vals[0][i] + S(p)*vals[1][i] + S(p-1)*vals[2][i] + S(p-2)*vals[3][i];
    }
    result = (int)(S(q+1)*tmpArr[0] + S(q)*tmpArr[1] + S(q-1)*tmpArr[2] + S(q-2)*tmpArr[3]);

    return result;
}
// 线性插值方法获取数据
static PyObject * linearInterpolation(PyObject * self, PyObject * args) {

    int v1, v2, v3, v4;
    float p, q;

    int result;

    if (! PyArg_ParseTuple(args, "(iiii)ff", &v1, &v2, &v3, &v4, &p, &q)) {
        return NULL;
    }
    
    result = linear(v1, v2, v3, v4, p, q);

    return Py_BuildValue("i", result);
}

static PyObject * cubicInterpolation(PyObject * self, PyObject * args) {
    int i;
    int ** vals = malloc(sizeof(int *)*4);
    for (i=0; i < 4; i++) {
        vals[i] = malloc(sizeof(int)*4);
    }

    float p, q;

    int result;

    if (! PyArg_ParseTuple(args, "((iiii)(iiii)(iiii)(iiii))ff", &vals[0][0], &vals[0][1], &vals[0][2], &vals[0][3], &vals[1][0], &vals[1][1], &vals[1][2], &vals[1][3], &vals[2][0], &vals[2][1], &vals[2][2], &vals[2][3], &vals[3][0], &vals[3][1], &vals[3][2], &vals[3][3], &p, &q)) {
        return NULL;
    }

    result = cubic(vals, p, q);

    return Py_BuildValue("i", result);
}

static PyMethodDef getValMethods[] = {
    {"linear", linearInterpolation, METH_VARARGS, "Linear Interpolation!"},
    {"cubic", cubicInterpolation, METH_VARARGS, "Cubic Interpolation!"},
    {NULL, NULL}
};

void initgetVal() {
    PyObject * m;
    m = Py_InitModule("getVal", getValMethods);
}
