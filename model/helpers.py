from typing import List, Tuple

def generateTrainingData() -> List[Tuple]:
  training_data = []
  technologies = ["react", "javascript", "python", "c", "c#", "elixir", "desenvolvimento web", "html", "css", "angular", "vue", "haskell"]
  # len tech = 12
  phrases = ["Há anos que trabalho com ", "Venho estudando e aplicando no trabalho o ", "Meu emprego envolve tecnologias como ", "Nos últimos anos, trabalhei em projetos com ", "Estou aprendendo a usar ", "Meus estudos envolvem ", "Mexo com ", "Estou estagiando e uso ", "No meu estágio, aprendi "]
  # phrases = 9


  for phrase in phrases:
    for tech in technologies:
      train_phr = f"{phrase}{tech}"
      idxStart = train_phr.find(tech)
      idxEnd = idxStart + len(tech)
      training_data.append((train_phr, [(idxStart, idxEnd, "TECH")]))

  return training_data