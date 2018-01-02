Controller
===================

Purpose
-------

A data collection system that accommodates diverse datatypes, storing either on the filesystem or within a sqlite table.

Scope
-----

Controller coordinates access to resources. Includes a poll of resources on a regular interval, along with a listener that accepts changes to the resource poll and provides access to stored resources.
