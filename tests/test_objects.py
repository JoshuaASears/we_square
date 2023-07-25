from desktop.data.schema import *


def add_objects():
    # create ledgers
    ledgers = []

    p1 = Person("Bob Holiday", "bobh@fake.email.com")
    p2 = Person("Hailey Jones", "hj@fakemail.com")

    t1 = Transaction("Dinner", "40.50", "1990-05-01", p2)
    t2 = Transaction("Movies", "18.50", "1990-05-01", p2)
    t3 = Transaction("Brews", "32.00", "1990-05-01", p1)
    t4 = Transaction("Cab", "15.00", "1990-05-01", p1)
    people = [p1, p2]
    l1 = Ledger("First Date", people)

    l1.add_transaction(t1)
    l1.add_transaction(t2)
    l1.add_transaction(t3)
    l1.add_transaction(t4)

    ledgers.append(l1)

    p1 = Person("Randy Marsh", "randy@sp.com")
    p2 = Person("Heath Ledger", "hl@dk.com")
    p3 = Person("Stanley Kubrick", "sfk@movie.god.com")

    t1 = Transaction("Go Karts", "350.00", "2008-04-01", p1)
    t2 = Transaction("Brewskies", "91.55", "2008-04-01", p2)
    t3 = Transaction("Hotdog Competition", "33.00", "2008-10-20", p3)
    t4 = Transaction("Lambos", "900,000.00", "2009-06-02", p2)
    t4.delete()
    t5 = Transaction("River Cruise", "1,800.00", "2011-10-19", p3)
    t5.set_amount("1,900.00")
    t6 = Transaction("Video Games", "60.00", "2012-08-30", p1)
    t7 = Transaction("Brews", "32.00", "2012-05-01", p1)
    t8 = Transaction("Golf", "800.00", "2013-07-26", p2)

    people = [p1, p2, p3]
    l2 = Ledger("Just cussin' around.", people)

    l2.add_transaction(t1)
    l2.add_transaction(t2)
    l2.add_transaction(t3)
    l2.add_transaction(t4)
    l2.add_transaction(t5)
    l2.add_transaction(t6)
    l2.add_transaction(t7)
    l2.add_transaction(t8)

    ledgers.append(l2)

    return ledgers
