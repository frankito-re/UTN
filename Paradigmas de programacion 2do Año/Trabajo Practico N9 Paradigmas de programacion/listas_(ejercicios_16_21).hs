longitudLista :: [a] -> Int
longitudLista [] = 0
longitudLista (_ : xs) = 1 + longitudLista xs

sumarImpares :: [Int] -> Int
sumarImpares [] = 0
sumarImpares (x : xs)
  | odd x = x + sumarImpares xs
  | otherwise = sumarImpares xs

sumaLista :: (Num a) => [a] -> a
sumaLista [] = 0
sumaLista (x : xs) = x + sumaLista xs

invertirLista :: [a] -> [a]
invertirLista [] = []
invertirLista (x : xs) = (invertirLista xs) ++ [x]

ultimoElementoPre :: [a] -> a
ultimoElementoPre = last

ultimoElementoRec :: [a] -> a
ultimoElementoRec [x] = x
ultimoElementoRec (_ : xs) = ultimoElementoRec xs
ultimoElementoRec [] = error "Lista vacia no tiene ultimo elemento"

contarLetra :: Char -> String -> Int
contarLetra _ "" = 0
contarLetra c (x : xs)
  | c == x = 1 + contarLetra c xs
  | otherwise = contarLetra c xs