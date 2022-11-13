# aied-project

MVP: (ran in terminal, no data saved between sessions)

1. Run in terminal
2. ** Asks for list of interests separated by commas
3. Turn that into initial interest list
4. create student model with empty graph, empty fringe, and student interest list
5. search for wiki articles of interests and any that exist, create WikiNode objects for them (with no prevNode) and add to fringe queue
6. ** Give user option between top 3 articles in fringe queue(input number for which one you want to read?)
7. ** Print content to terminal so they can read it
8. call updateGraph() with that WikiNode they selected
9. update fringe with linked articles from that article
    -- still need to iron out how exactly this works... something with the key words? possibly using categories somehow to rank them?
    -- include using heuristic based on breadth or subject targetting as well??
10. Repeat steps 6-9 forever