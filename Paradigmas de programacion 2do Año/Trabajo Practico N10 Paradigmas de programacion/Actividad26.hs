quicksort :: (Ord a) => [a] -> [a]
quicksort [] = []
quicksort (x:xs) =
  let menores = filter (< x) xs
      mayores = filter (>= x) xs
  in quicksort menores ++ [x] ++ quicksort mayores

main :: IO ()
main = print (quicksort [3,7,2,9,1,5])