# Makefile for source rpm: dev86
# $Id$
NAME := dev86
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
