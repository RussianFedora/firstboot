# Makefile for source rpm: firstboot
# $Id$
NAME := firstboot
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
