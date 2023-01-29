package main

import (
	"flag"
	"time"

	"golang.org/x/exp/rand"
	"gonum.org/v1/gonum/mat"
	"gonum.org/v1/gonum/stat/distuv"
)

type programParameters struct {
	N               int
	trials          int
	multiplications int
	threads         int
	matrix          mat.Matrix
}

func heaviside(vector *mat.VecDense) {
	for n := 0; n < vector.Len(); n++ {
		if vector.AtVec(n) <= 0 {
			vector.SetVec(n, -1)
		} else {
			vector.SetVec(n, 1)
		}
	}
}

func thread_func(params programParameters, indexChannel chan int) {
	randSrc := rand.NewSource(uint64(time.Now().UnixNano()))
	normalDistribution := distuv.Normal{
		Mu:    0,
		Sigma: 1,
		Src:   randSrc,
	}
	vectorData := make([]float64, params.N)
	for range indexChannel {
		for i := range vectorData {
			vectorData[i] = normalDistribution.Rand()
		}
		vector := mat.NewVecDense(params.N, vectorData)
		heaviside(vector)
		for j := 0; j < params.multiplications; j++ {
			vector.MulVec(params.matrix, vector)
			heaviside(vector)
		}
	}
}

func main() {

	N := flag.Int("n", 100, "Size of matrix and vector")
	trials := flag.Int("trials", 1000, "The number of trials to attempt")
	multiplications := flag.Int("multiplications", 1000, "The number of multiplications to use for each trial")
	threads := flag.Int("threads", 1, "The number of threads to use for each trial")
	flag.Parse()

	randSrc := rand.NewSource(uint64(time.Now().UnixNano()))
	normalDistribution := distuv.Normal{
		Mu:    0,
		Sigma: 1,
		Src:   randSrc,
	}
	matrixData := make([]float64, *N**N)
	for i := range matrixData {
		matrixData[i] = normalDistribution.Rand()
	}
	matrix := mat.NewDense(*N, *N, matrixData)

	params := programParameters{
		*N,
		*trials,
		*multiplications,
		*threads,
		matrix,
	}

	indexChannel := make(chan int, 10)
	for i := 0; i < *threads; i++ {
		go thread_func(params, indexChannel)
	}

	for i := 0; i < *trials; i++ {
		// println(i)
		indexChannel <- i
	}
	close(indexChannel)
}
