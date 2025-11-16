len :: [a] -> Int
len xs = sum [1 | _ <- xs]

main :: IO ()
main = print (len [1,2,3,4,5])