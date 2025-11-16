calcularPromedio :: [Float] -> Float
calcularPromedio xs = sum xs / fromIntegral (length xs)

main :: IO ()
main = print (calcularPromedio [4,6,8,10])