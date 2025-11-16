filtrarParesv1 :: [Int] -> [Int]
filtrarParesv1 xs = filter esPar xs
  where
    esPar x = x `mod` 2 == 0

filtrarParesv2 :: [Int] -> [Int]
filtrarParesv2 = filter (\x -> x `mod` 2 == 0)

main :: IO ()
main = do
    print (filtrarParesv1 [1,2,3,4,5,6])
    print (filtrarParesv2 [1,2,3,4,5,6])