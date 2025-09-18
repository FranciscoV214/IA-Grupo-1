(define (domain ROBOT)
  (:requirements :strips :typing)

  (:types robot obj box room)

  (:predicates 
    (box ?b - box)
    (room ?x - room)
    (robot ?r - robot)
    (obj ?o - obj)
    (gripper ?r - robot)             ; el robot tiene las manos libres
    (at ?x - (either robot obj box) ?r - room) ; algo está en un lugar
    (in_box ?o - obj ?b - box)       ; objeto dentro de caja
    (carry ?r - robot ?o - obj)      ; robot lleva un objeto
  )

  (:action move
    :parameters (?r - robot ?from - room ?to - room)
    :precondition (and (at ?r ?from))
    :effect (and (not (at ?r ?from)) (at ?r ?to))
  )

  (:action pick
    :parameters (?o - obj ?x - room ?r - robot)
    :precondition (and (at ?r ?x) (at ?o ?x) (gripper ?r))
    :effect (and (carry ?r ?o) (not (gripper ?r)) (not (at ?o ?x)))
  )

  (:action drop_in_box
    :parameters (?o - obj ?r - robot ?b - box ?x - room)
    :precondition (and (at ?r ?x) (at ?b ?x) (carry ?r ?o))
    :effect (and (in_box ?o ?b) (gripper ?r) (not (carry ?r ?o)))
  )
)
