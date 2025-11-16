calcularCuadradosv1 :: [Int] -> [Int]
calcularCuadradosv1 xs = map cuadrado xs
  where
    cuadrado x = x * x

calcularCuadradosv2 :: [Int] -> [Int]
calcularCuadradosv2 = map (\x -> x * x)

main :: IO ()
main = do
    print (calcularCuadradosv1 [1,2,3,4])
    print (calcularCuadradosv2 [1,2,3,4])
    