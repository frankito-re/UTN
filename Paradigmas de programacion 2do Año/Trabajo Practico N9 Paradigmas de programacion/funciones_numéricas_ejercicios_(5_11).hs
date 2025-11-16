sumaDos :: Double -> Double -> Double
sumaDos x y = x + y

distanciaPuntos :: (Double, Double) -> (Double, Double) -> Double
distanciaPuntos (x1, y1) (x2, y2) = sqrt ((x2 - x1) ^ 2 + (y2 - y1) ^ 2)

hipotenusa :: Double -> Double -> Double
hipotenusa a b = sqrt (a ^ 2 + b ^ 2)

esPositivo :: Double -> Bool
esPositivo n = n > 0

duplicarSiMenorCien :: Double -> Double
duplicarSiMenorCien n
  | n < 100 = n * 2
  | otherwise = n

mayorDeDos :: (Ord a) => a -> a -> a
mayorDeDos x y
  | x >= y = x
  | otherwise = y

signo :: (Num a, Ord a) => a -> Int
signo x
  | x > 0 = 1
  | x == 0 = 0
  | x < 0 = -1