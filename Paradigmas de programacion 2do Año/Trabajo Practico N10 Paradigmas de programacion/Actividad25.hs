transformar :: [Int] -> [Int]
transformar xs = map (\x -> x * 2 + 3) xs

main :: IO ()
main = print (transformar [1,2,3])
