module Jekyll
  class Preprocessing < Jekyll::Generator
    def generate(site)
      system 'cd _tasks; make; cd ..'
    end
  end
end
