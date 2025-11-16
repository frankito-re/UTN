cuadrarLista :: [Int] -> [Int]
cuadrarLista xs = [x^2 | x <- xs]

main :: IO ()
main = print (cuadrarLista [1,2,3,4])