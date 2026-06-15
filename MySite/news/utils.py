class MyMixin(object):
    mixin_prop = "hello world"

    def get_prop(self):
        return self.mixin_prop.upper()

    # Преобразовать переданный аргумент в верхний регистр.
    def get_upper(self, s):
        if isinstance(s, str):
            return s.upper()
        return s.title.upper()