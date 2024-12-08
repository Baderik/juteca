from database.models import User, Group

from keyboards.default.group import group_page_keyboard


def _group(num: int) -> str:
    if num == 0 and num >= 5:
        return f"Нашлось {num} групп"
    if num == 1:
        return f"Нашлась {num} группа"
    if num >= 2:
        return f"Нашлось {num} группы"


def _text(page_data: list[Group], search: str, count: int, page: int, page_size: int) -> str:
    head = _group(count)
    if search:
        head += f" Запрос: {search}"
    page_count = (count - 1) // page_size + 1 if count else 0
    page_txt = "\n".join([f"---\n{group.head}\n{group.desc}" for group in page_data])
    if page_txt:
        page_txt = "\n" + page_txt
    return (f"{head}\n"
            f"Стр {page}/{page_count}"
            f"{page_txt}")


async def get_page(user: User, search: str, page: int, page_size: int):
    await user.fetch_related("owned_groups", "groups")
    data = Group.filter(name__icontains=search).order_by("name")
    offset = max(0, (page - 1) * page_size)
    page_data = await data.offset(offset).limit(page_size)
    count = await data.count()
    before_page = page - 1
    last_page = (count - 1) // page_size + 1
    next_page = 0 if page == last_page else page + 1
    return {
        "text": _text(page_data, search, count, page, page_size),
        "reply_markup": group_page_keyboard(user, page_data, search, before_page, next_page)
    }
