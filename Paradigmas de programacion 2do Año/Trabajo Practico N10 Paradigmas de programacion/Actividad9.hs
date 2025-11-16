mayores10 :: [Int] -> [Int]
mayores10 xs = [x | x <- xs, x > 10]

main :: IO ()
main = print (mayores10 [4,15,22,7])