doblar :: Int -> Int
doblar x = x * 2

doblarNumerosv1 :: [Int] -> [Int]
doblarNumerosv1 xs = map doblar xs

doblarNumerosv2 :: [Int] -> [Int]
doblarNumerosv2 xs = map (\x -> x * 2) xs

main :: IO ()
main = do
    print (doblarNumerosv1 [1,2,3,4])
    print (doblarNumerosv2 [5,10,15])
