def val_date_not_past(selected_date):
    from datetime import datetime
    try:
        selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
        today = datetime.now().date()
        if selected_date < today:
            return False
    except ValueError:
        print("{dynamic_texts.orderdatewarning.text}")
        return False

    return True
