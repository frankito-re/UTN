factorial :: Int -> Int
factorial 0 = 1
factorial n = n * factorial (n - 1)

fibonacci :: Int -> Int
fibonacci 0 = 0
fibonacci 1 = 1
fibonacci n = fibonacci (n - 1) + fibonacci (n - 2)

mult :: Int -> Int -> Int
mult x 0 = 0
mult x y = x + mult x (y - 1)

sumarUno :: Int -> Int
sumarUno n = n + 1

sumaRecursiva :: Int -> Int -> Int
sumaRecursiva x 0 = x
sumaRecursiva x y = sumarUno (sumaRecursiva x (y - 1))