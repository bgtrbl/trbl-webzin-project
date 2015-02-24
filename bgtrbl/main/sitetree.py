from sitetree.utils import tree, item

sitetrees = (
        tree("root", item =[
            item("Main", "main"),
            item("Articles", "trblcms.articles"),
            itme("Post", "trblcms.add_article"), 
            item("Login", "accounts"),
            item("Goal", "main.goal"),
            item("About", "main.about")
            ]
            )
        )



