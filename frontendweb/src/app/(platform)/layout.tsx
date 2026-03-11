import React from 'react'
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const Layout = ({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) => {
  return (
    <div>{children}</div>
  )
}

export default Layout