repetirA :: Int -> String
repetirA 0 = ""
repetirA n = "a" ++ repetirA (n - 1)

repetirChar :: Char -> Int -> String
repetirChar _ 0 = ""
repetirChar c n = [c] ++ repetirChar c (n - 1)

primera :: String -> Char
primera [] = error "String vacío"
primera (x : _) = x

duplicarPrimero :: [a] -> [a]
duplicarPrimero [] = []
duplicarPrimero (x : xs) = x : x : xs

estaEnLista :: (Eq a) => a -> [a] -> Bool
estaEnLista _ [] = False
estaEnLista e (x : xs)
  | e == x = True
  | otherwise = estaEnLista e xs