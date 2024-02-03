This is a project intending on looking at prices and card trends.

The end goal is to build a tool that:
1) Analyzes your cards from a pool of card stores to determine the optimal site to sell your cards to.
2) Preps the cart for you to sell your cards through the site so the user does not need to manually add all the cards 

List of sets retrieved from: https://mtgjson.com/

Attempting on completing this project using Builder pattern. Builder will select which scraper to use and prep the data.


                                 Builder     ←       CardData
                                    ↓
                                ←       →
                            ↓               ↓
                        ScraperA        ScraperB
                            ↓               ↓
                          result          result                           