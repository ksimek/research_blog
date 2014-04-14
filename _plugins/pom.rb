require 'date'
module Jekyll
  class PomodoroPath < Liquid::Tag
# Simple tag that returns the path to a post's pomodoro entry
#
    def initialize(tag_name, text, tokens)
      super
      @text = text
    end

    def render(context)
      page = context['page']
      if page.has_key?('date')
        date = page['date']
        path = to_pomodoro_path(date)
#        String.try_convert(context['site']['baseurl']).class
        a = context['site']['baseurl'].to_s + '/' + path
        a
      end
    end

    def to_pomodoro_path(date)
    # convert date to URL for pomodoro entry
    # This will likely change in the future, hence the need
    # for a generic solution
        return sprintf("pomodoro.html#%04d_%02d_%02d", date.year, date.month, date.day)
    end
  end
end

Liquid::Template.register_tag('pomodoro_path', Jekyll::PomodoroPath)
