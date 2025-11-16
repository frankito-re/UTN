aplicarALista :: (a -> b) -> [a] -> [b]
aplicarALista _ [] = []
aplicarALista f (x:xs) = f x : aplicarALista f xs

main :: IO ()
main = print (aplicarALista (*2) [1,2,3])