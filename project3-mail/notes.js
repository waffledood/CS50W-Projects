const ex;

ex.addEventListener('click', () => f1(para1));
ex.addEventListener('click', () => f2(para1, para2));
ex.addEventListener('click', f1);
ex.addEventListener('click', () => {
                                    f1(para1);
                                    f2(para1, para2)
                                    });

// anonymous function
ex.addEventListener('click', function() {
                                          // do something
                                        });


// can't recall how the following one is set up, in terms of the variable in brackets ()
ex.addEventListener('click', (variable) => f1(para1));