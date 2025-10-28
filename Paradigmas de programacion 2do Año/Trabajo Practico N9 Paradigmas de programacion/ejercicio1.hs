sumarpares (x : xs) =
  if x rem 2 == 0
    then
      x + sumarpares []
    else
      sumarpares []