imparesMayores5 :: [Int] -> [Int]
imparesMayores5 xs = [x | x <- xs, odd x, x > 5]

main :: IO ()
main = print (imparesMayores5 [3,6,7,9,12])